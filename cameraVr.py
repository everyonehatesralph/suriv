import cv2
import time
from pathlib import Path
from datetime import datetime


def open_camera(index: int, width: int | None = None, height: int | None = None) -> cv2.VideoCapture:
    """
    Open a camera device reliably across Windows/macOS/Linux.
    Tries CAP_DSHOW on Windows for faster init; falls back if needed.
    """
    # Try DirectShow first (best for many Windows setups)
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera at index {index}.")

    if width is not None:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(width))
    if height is not None:
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(height))

    return cap


def warmup_camera(cap: cv2.VideoCapture, seconds: float = 1.0) -> None:
    """
    Read frames for a short time to allow auto-exposure/auto-focus to stabilize.
    """
    end = time.time() + seconds
    while time.time() < end:
        ok, _ = cap.read()
        if not ok:
            time.sleep(0.01)


def timestamp_name(prefix: str = "capture", ext: str = "jpg") -> str:
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.{ext}"


def main(
    camera_index: int = 0,
    out_dir: str = "captures",
    warmup_seconds: float = 1.0,
    initial_delay_seconds: float = 0.5,
    count: int = 1,
    interval_seconds: float = 0.5,
    show_preview: bool = True,
    width: int | None = None,
    height: int | None = None,
) -> None:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    cap = open_camera(camera_index, width=width, height=height)

    try:
        warmup_camera(cap, warmup_seconds)
        time.sleep(max(0.0, initial_delay_seconds))

        for i in range(count):
            ok, frame = cap.read()
            if not ok or frame is None:
                raise RuntimeError("Failed to read frame from camera.")

            filename = timestamp_name(prefix=f"capture_{i+1}")
            save_path = out_path / filename

            # Write image to disk (BGR is correct for cv2.imwrite)
            if not cv2.imwrite(str(save_path), frame):
                raise RuntimeError(f"Failed to write image to {save_path}")

            print(f"Saved: {save_path.resolve()}")

            if show_preview:
                cv2.imshow("Auto Capture (ESC to abort)", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    print("Aborted by user (ESC).")
                    break

            if i < count - 1:
                # Wait before next capture; allow ESC abort during wait if preview enabled
                end = time.time() + max(0.0, interval_seconds)
                while time.time() < end:
                    if show_preview:
                        # Keep window responsive; allow ESC during interval
                        if (cv2.waitKey(1) & 0xFF) == 27:
                            print("Aborted by user (ESC).")
                            return
                    time.sleep(0.01)

    finally:
        cap.release()
        if show_preview:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    # Example defaults: 1 photo after warmup
    main(
        camera_index=0,
        out_dir="captures",
        warmup_seconds=1.0,
        initial_delay_seconds=0.5,
        count=1,
        interval_seconds=0.5,
        show_preview=True,
        width=None,
        height=None,
    )