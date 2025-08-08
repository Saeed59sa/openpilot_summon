from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
  import cv2
except Exception:  # pragma: no cover - handled gracefully at runtime
  cv2 = None

from .sdracemode_settings import SDRaceModeSettings


VIDEO_DIR = Path("/data/sdracemode/videos")


class SDRaceRecorder:
  """Simple video (and optional audio) recorder for SDRaceMode."""

  def __init__(self, settings: SDRaceModeSettings) -> None:
    self.settings = settings
    self.video_writer: Optional[cv2.VideoWriter] = None
    self.capture: Optional[cv2.VideoCapture] = None
    self.audio_proc: Optional[subprocess.Popen] = None
    self.output_path: Optional[Path] = None

  def _detect_microphone(self) -> Optional[str]:
    # Very lightweight detection: prefer any device containing "USB" in its
    # ALSA name; fallback to default.
    try:
      devices = subprocess.check_output(["arecord", "-l"], text=True)
    except Exception:
      return None
    for line in devices.splitlines():
      if "USB" in line:
        return "plug:default"
    return None

  def start(self) -> Path:
    if cv2 is None:
      raise RuntimeError("cv2 is required for video recording")

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    self.output_path = VIDEO_DIR / f"sdracemode_{timestamp}.mp4"

    self.capture = cv2.VideoCapture(0)
    fps = self.capture.get(cv2.CAP_PROP_FPS) or 20.0
    width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    self.video_writer = cv2.VideoWriter(str(self.output_path), fourcc, fps, (width, height))

    mic = None
    if self.settings.record_audio != "0":
      mic = self._detect_microphone()
    if mic:
      audio_path = str(self.output_path.with_suffix(".wav"))
      self.audio_proc = subprocess.Popen(["arecord", "-f", "cd", audio_path])
    return self.output_path

  def write_frame(self) -> None:
    if not self.capture or not self.video_writer:
      return
    ret, frame = self.capture.read()
    if ret:
      self.video_writer.write(frame)

  def stop(self) -> Optional[Path]:
    if self.video_writer:
      self.video_writer.release()
    if self.capture:
      self.capture.release()
    if self.audio_proc:
      self.audio_proc.terminate()
      self.audio_proc = None
    return self.output_path
