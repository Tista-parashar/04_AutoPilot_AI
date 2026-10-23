
"""Record a video with steering-output overlays."""

import cv2
import numpy as np
from pathlib import Path


def main():
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "demo.mp4"
    width, height = 640, 480
    fps = 20
    duration_seconds = 30

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        str(output_path), fourcc, fps, (width, height)
    )

    if not writer.isOpened():
        raise RuntimeError("Could not create demo.mp4")

    try:
        for frame_number in range(fps * duration_seconds):
            frame = np.zeros((height, width, 3), dtype=np.uint8)

            # Placeholder values only. These are NOT model predictions.
            steer = 0.0
            cv2.putText(
                frame,
                "AutoPilot AI - Recording Pipeline Test",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                frame,
                f"steer: {steer:.2f} (placeholder)",
                (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
            )
            cv2.putText(
                frame,
                f"Time: {frame_number / fps:.1f}s",
                (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            writer.write(frame)
    finally:
        writer.release()

    print(f"Recording saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
