
"""Bridge utilities for connecting AutoPilot AI to CARLA."""

import numpy as np
import onnxruntime as ort
from PIL import Image

from src.controller import PIDController


def preprocess_camera_image(image):
    """Convert a CARLA BGRA image into a normalized NumPy batch."""
    image_array = np.frombuffer(image.raw_data, dtype=np.uint8)
    image_array = image_array.reshape(
        (image.height, image.width, 4)
    )

    # Convert BGRA to RGB.
    rgb_image = image_array[:, :, :3][:, :, ::-1].copy()

    # Resize using bilinear interpolation, matching the previous pipeline.
    resized_image = Image.fromarray(rgb_image).resize(
        (224, 224),
        resample=Image.Resampling.BILINEAR,
    )

    # Convert to float32, scale to [0, 1], then normalize to [-1, 1].
    image_array = np.asarray(resized_image, dtype=np.float32) / 255.0
    image_array = (image_array - 0.5) / 0.5

    # Convert HWC to NCHW: (1, 3, 224, 224).
    image_array = np.transpose(image_array, (2, 0, 1))
    return np.expand_dims(image_array, axis=0).astype(np.float32)


def load_onnx_model(model_path="models/model.onnx"):
    """Load the ONNX model for CPU inference."""
    return ort.InferenceSession(
        model_path,
        providers=["CPUExecutionProvider"],
    )


def run_inference(session, image_batch):
    """Run ONNX inference using a NumPy image batch."""
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    outputs = session.run(
        [output_name],
        {input_name: np.asarray(image_batch, dtype=np.float32)},
    )

    return outputs[0][0]


def create_control_controllers():
    """Create separate PID controllers for steering and speed."""
    steering_pid = PIDController(
        kp=0.5,
        ki=0.01,
        kd=0.1,
        output_limits=(-1.0, 1.0),
    )

    speed_pid = PIDController(
        kp=0.1,
        ki=0.01,
        kd=0.01,
        output_limits=(-1.0, 1.0),
    )

    return steering_pid, speed_pid


def calculate_control(
    steering_error,
    target_speed_kmh,
    current_speed_kmh,
    dt,
    steering_pid,
    speed_pid,
):
    """Calculate control suggestions without moving a vehicle."""
    steering = steering_pid.update(steering_error, dt)

    speed_error = target_speed_kmh - current_speed_kmh
    speed_correction = speed_pid.update(speed_error, dt)

    return {
        "steering": steering,
        "speed_error_kmh": speed_error,
        "speed_correction": speed_correction,
    }
