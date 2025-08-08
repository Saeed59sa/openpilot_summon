from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from common.params import Params

from .sdracemode_autoconfig import SDRAutoConfig
from .sdracemode_disclaimer import check_disclaimer
from .sdracemode_evcontrols import SDRaceEVControls
from .sdracemode_recorder import SDRaceRecorder
from .sdracemode_settings import SDRaceModeSettings
from .sdracemode_ui import SDRaceModeUI


SESSION_DIR = Path("/data/sdracemode/sessions")


class SDRaceMode:
  """Main runtime controller for SDRaceMode."""

  def __init__(self) -> None:
    self.params = Params()
    self.settings = SDRaceModeSettings(self.params)
    self.ui = SDRaceModeUI(self.settings)
    self.recorder = SDRaceRecorder(self.settings)
    self.ev_controls = SDRaceEVControls(self.settings)
    self.autoconfig = SDRAutoConfig(self.params)
    self.car_params: Dict[str, Any] | None = None
    self.fingerprint: str = ""

  def start(self, car_params: Dict[str, Any], fingerprint: str) -> bool:
    self.car_params = car_params
    self.fingerprint = fingerprint
    self.autoconfig.configure(car_params, fingerprint)

    if not check_disclaimer(self.params):
      return False

    self.settings.enabled = True
    self.ev_controls.apply()
    self.recorder.start()
    return True

  def update(self, frame, stats: Dict[str, Any]) -> Any:
    """Update UI and write current frame to the recorder."""
    self.recorder.write_frame()
    return self.ui.draw(frame, stats)

  def stop(self, results: Dict[str, Any]) -> Path | None:
    video_path = self.recorder.stop()
    self.settings.enabled = False

    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    session = {
      "vin": self.car_params.get("vin") if self.car_params else None,
      "fingerprint": self.fingerprint,
      "timestamp": datetime.utcnow().isoformat(),
      "results": results,
      "video": str(video_path) if video_path else None,
    }
    session_path = SESSION_DIR / f"session_{int(time.time())}.json"
    with open(session_path, "w", encoding="utf-8") as f:
      json.dump(session, f, indent=2)
    return video_path
