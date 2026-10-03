import matplotlib.pyplot as plt

epochs = list(range(1, 11))

train_losses = [
    0.217896,
    0.740878,
    0.754477,
    0.172940,
    0.086068,
    0.057128,
    0.043184,
    0.036141,
    0.032501,
    0.030604
]

val_losses = [
    0.100554,
    0.170217,
    4.815784,
    4.689034,
    2.736627,
    1.642652,
    1.087461,
    0.773344,
    0.600291,
    0.491504
]

plt.figure(figsize=(8, 5))

plt.plot(epochs, train_losses, marker="o", label="Train Loss")
plt.plot(epochs, val_losses, marker="o", label="Validation Loss")

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training vs Validation Loss")
plt.legend()
plt.grid(True)

plt.savefig("reports/loss_curve.png")

print("Loss curve saved!")