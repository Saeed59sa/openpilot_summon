from __future__ import annotations

try:
  import cv2
  import numpy as np
except Exception:  # pragma: no cover - optional dependency
  cv2 = None
  np = None

from .sdracemode_settings import SDRaceModeSettings


class SDRaceModeUI:
  """Overlay HUD for SDRaceMode using OpenCV."""

  def __init__(self, settings: SDRaceModeSettings) -> None:
    self.settings = settings

  def draw(self, frame, stats: dict) -> any:
    """Draw overlays on the given frame.

    Parameters
    ----------
    frame: numpy.ndarray
      Frame from camera.
    stats: dict
      Dictionary with live data: speed, g_force, power, torque, timers.
    """
    if cv2 is None:
      return frame

    overlay = frame.copy()
    h, w, _ = frame.shape

    speed = stats.get("speed", 0)
    cv2.putText(overlay, f"{speed:.0f} km/h", (w // 2 - 50, h - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

    if self.settings.enable_drift:
      cv2.putText(overlay, "DRIFT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                  0.8, (0, 0, 255), 2)

    g = stats.get("g_force", 0)
    cv2.putText(overlay, f"G {g:.2f}", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 0), 1)

    return overlay

  def summary_screen(self, results: dict) -> np.ndarray:
    """Return an image with session summary."""
    if cv2 is None or np is None:
      raise RuntimeError("cv2 and numpy are required for summary display")

    img = np.zeros((480, 800, 3), dtype=np.uint8)
    cv2.putText(img, "SDRaceMode Results", (100, 60), cv2.FONT_HERSHEY_SIMPLEX,
                1.2, (255, 255, 255), 2)
    lines = [
      f"0-60: {results.get('0_60', 'n/a')} s",
      f"0-100: {results.get('0_100', 'n/a')} s",
      f"100-200: {results.get('100_200', 'n/a')} s",
      f"Peak G: {results.get('g_peak', 'n/a')}",
      f"Max power: {results.get('max_power', 'n/a')} {self.settings.power_unit}",
    ]
    y = 150
    for line in lines:
      cv2.putText(img, line, (80, y), cv2.FONT_HERSHEY_SIMPLEX,
                  0.9, (255, 255, 255), 2)
      y += 60
    return img
