import sys
import os
import torch

sys.path.append(os.path.abspath("."))

from src.model import AutoPilotModel


def test_model_initialization():
    model = AutoPilotModel()
    assert model is not None


def test_forward_pass():
    model = AutoPilotModel()

    dummy = torch.randn(1, 3, 256, 256)

    out = model(dummy)

    assert out.requires_grad
    assert out.shape == (1, 3)


def test_cuda_availability():
    assert torch.cuda.is_available() is False
    