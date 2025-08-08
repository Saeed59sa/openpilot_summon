"""Video and audio recording utilities for SDRaceMode."""
from __future__ import annotations
import os
import time
from typing import Optional

try:
    import cv2  # type: ignore
except Exception:  # pragma: no cover
    cv2 = None


class SDRaceModeRecorder:
    """Simple video recorder using OpenCV if available."""
    def __init__(self, out_dir: str = "/data/sdracemode/videos") -> None:
        self.out_dir = out_dir
        self.writer: Optional["cv2.VideoWriter"] = None
        self.out_file: Optional[str] = None

    def start(self) -> None:
        os.makedirs(self.out_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        self.out_file = os.path.join(self.out_dir, f"{timestamp}.mp4")
        if cv2 is None:
            return
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.writer = cv2.VideoWriter(self.out_file, fourcc, 20.0, (640, 480))

    def write_frame(self, frame) -> None:
        if self.writer is not None:
            self.writer.write(frame)

    def stop(self) -> Optional[str]:
        if self.writer is not None:
            self.writer.release()
            self.writer = None
        return self.out_file
