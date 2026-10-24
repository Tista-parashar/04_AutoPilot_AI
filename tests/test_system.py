
"""System-level tests for the AutoPilot AI integration."""

import os
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
from PIL import Image

from src.carla_bridge import (
    calculate_control,
    create_control_controllers,
    load_onnx_model,
    preprocess_camera_image,
    run_inference,
)

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "data" / "cleaned"
MODEL_PATH = ROOT / "models" / "model.onnx"


def get_project_image():
    """Load an existing project image instead of inventing test imagery."""
    candidates = []
    for extension in ("*.jpg", "*.jpeg", "*.png"):
        candidates.extend(IMAGE_DIR.glob(extension))

    if not candidates:
        pytest.skip("No JPG or PNG images found in data/cleaned.")

    with Image.open(candidates[0]) as image:
        return image.convert("RGB").copy()


def make_camera_buffer(image):
    """Adapt an existing project image to the bridge's CARLA camera format."""
    rgb = np.asarray(image, dtype=np.uint8)
    bgra = np.dstack(
        (
            rgb[:, :, ::-1],
            np.full((*rgb.shape[:2], 1), 255, dtype=np.uint8),
        )
    )

    return SimpleNamespace(
        raw_data=bgra.tobytes(),
        width=image.width,
        height=image.height,
    )


def test_camera_preprocessing():
    image = get_project_image()
    camera_image = make_camera_buffer(image)

    batch = preprocess_camera_image(camera_image)

    assert batch.shape == (1, 3, 224, 224)
    assert batch.dtype == np.float32
    assert np.isfinite(batch).all()
    assert batch.min() >= -1.0
    assert batch.max() <= 1.0


def test_onnx_inference():
    if not MODEL_PATH.is_file():
        pytest.fail(f"ONNX model not found: {MODEL_PATH}")

    image = get_project_image()
    camera_image = make_camera_buffer(image)
    batch = preprocess_camera_image(camera_image)

    session = load_onnx_model(str(MODEL_PATH))
    prediction = run_inference(session, batch)

    assert prediction.shape == (3,)
    assert np.isfinite(prediction).all()


def test_control_suggestions_are_bounded():
    steering_pid, speed_pid = create_control_controllers()

    result = calculate_control(
        steering_error=0.2,
        target_speed_kmh=30.0,
        current_speed_kmh=20.0,
        dt=0.05,
        steering_pid=steering_pid,
        speed_pid=speed_pid,
    )

    assert -1.0 <= result["steering"] <= 1.0
    assert -1.0 <= result["speed_correction"] <= 1.0
    assert result["speed_error_kmh"] == 10.0


@pytest.fixture
def carla_world():
    """Connect to CARLA, or skip genuine simulator tests if unavailable."""
    carla = pytest.importorskip(
        "carla",
        reason="CARLA Python API is not installed.",
    )

    host = os.getenv("CARLA_HOST", "127.0.0.1")
    port = int(os.getenv("CARLA_PORT", "2000"))

    client = carla.Client(host, port)
    client.set_timeout(3.0)

    try:
        world = client.get_world()
        original_weather = world.get_weather()
    except Exception as exc:
        pytest.skip(f"CARLA server is unavailable: {exc}")

    yield carla, world

    try:
        world.set_weather(original_weather)
    except Exception:
        pass


@pytest.mark.parametrize(
    ("scenario", "weather_name"),
    [
        ("sunny", "ClearNoon"),
        ("rainy", "WetCloudyNoon"),
        ("night", "ClearNight"),
    ],
)
def test_carla_weather_scenario(carla_world, scenario, weather_name):
    carla, world = carla_world

    weather = getattr(carla.WeatherParameters, weather_name)
    world.set_weather(weather)
    actual = world.get_weather()

    if scenario == "sunny":
        assert actual.sun_altitude_angle > 0
    elif scenario == "rainy":
        assert actual.precipitation > 0
    elif scenario == "night":
        assert actual.sun_altitude_angle < 0


def test_carla_heavy_traffic_scenario(carla_world):
    _, world = carla_world

    vehicle_blueprints = list(
        world.get_blueprint_library().filter("vehicle.*")
    )
    spawn_points = world.get_map().get_spawn_points()

    if len(spawn_points) < 5 or not vehicle_blueprints:
        pytest.skip("CARLA map lacks enough vehicle spawn resources.")

    spawned_vehicles = []

    try:
        for index, spawn_point in enumerate(spawn_points):
            blueprint = vehicle_blueprints[
                index % len(vehicle_blueprints)
            ]
            vehicle = world.try_spawn_actor(blueprint, spawn_point)

            if vehicle is not None:
                spawned_vehicles.append(vehicle)

            if len(spawned_vehicles) >= 5:
                break

        assert len(spawned_vehicles) >= 5, (
            "Could not spawn five vehicles for the traffic scenario."
        )

        for vehicle in spawned_vehicles:
            vehicle.set_autopilot(True)

    finally:
        for vehicle in spawned_vehicles:
            try:
                if vehicle.is_alive:
                    vehicle.destroy()
            except Exception:
                pass
