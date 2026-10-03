from torchinfo import summary
from model import AutoPilotModel
import sys

model = AutoPilotModel()

with open("reports/model_summary.txt", "w", encoding="utf-8") as f:
    sys.stdout = f

    summary(
        model,
        input_size=(1, 3, 256, 256)
    )

    sys.stdout = sys.__stdout__

print("Model summary saved!")
