
"""Bridge utilities for connecting AutoPilot AI to CARLA."""

import numpy as np
import torch
from torchvision import transforms
from src.controller import PIDController


def preprocess_camera_image(image):
    """Convert a CARLA RGB image into a ResNet-compatible tensor."""
    image_array = np.frombuffer(image.raw_data, dtype=np.uint8)
    image_array = image_array.reshape(
        (image.height, image.width, 4)
    )

    # CARLA camera data uses BGRA channel order.
    rgb_image = image_array[:, :, :3][:, :, ::-1].copy()

    image_tensor = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5],
                             [0.5, 0.5, 0.5]),
    ])(rgb_image)

    return image_tensor.unsqueeze(0)

import onnxruntime as ort


def load_onnx_model(model_path="models/model.onnx"):
    """Load the ONNX model for CPU inference."""
    session = ort.InferenceSession(
        model_path,
        providers=["CPUExecutionProvider"],
    )
    return session

def run_inference(session, image_tensor):
    """Run ONNX inference on a preprocessed camera image."""
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    image_array = image_tensor.detach().cpu().numpy()

    outputs = session.run(
        [output_name],
        {input_name: image_array},
    )

    return outputs[0][0]
def create_control_controllers():
    """Create separate PID controllers for steering and speed."""
    steering_pid = PIDController(
        kp=0.5,
        ki=0.01,
        kd=0.05,
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