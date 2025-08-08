"""Main activation logic for SDRaceMode."""
from __future__ import annotations
import json
import os
import time
from typing import Optional

from common.params import Params

from .sdracemode_disclaimer import ensure_disclaimer
from .sdracemode_recorder import SDRaceModeRecorder
from .sdracemode_ui import SDRaceModeUI
from .sdracemode_evcontrols import EVController
from .sdracemode_settings import SettingsManager


class SDRaceMode:
    """Coordinates SDRaceMode components."""
    def __init__(self) -> None:
        self.params = Params()
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.load()
        self.ui = SDRaceModeUI()
        self.recorder = SDRaceModeRecorder()
        self.ev_controller = EVController()
        self.running = False
        self.start_time: Optional[float] = None
        self.start_time_100: Optional[float] = None
        self.results = {
            "0_60": None,
            "0_100": None,
            "100_200": None,
            "peak_torque": 0.0,
            "peak_power": 0.0,
            "g_force_max": 0.0,
        }

    def start(self) -> bool:
        if not self.settings.enable:
            return False
        if not ensure_disclaimer():
            return False
        self.ev_controller.apply_settings()
        self.recorder.start()
        self.ui.start()
        self.running = True
        self.start_time = time.time()
        return True

    def update(self, speed_kph: float, torque_nm: float, power_kw: float, g_force: float) -> None:
        if not self.running:
            return
        now = time.time()
        if self.start_time is None:
            self.start_time = now
        elapsed = now - self.start_time
        if speed_kph >= 60 and self.results["0_60"] is None:
            self.results["0_60"] = elapsed
        if speed_kph >= 100 and self.results["0_100"] is None:
            self.results["0_100"] = elapsed
            if self.start_time_100 is None:
                self.start_time_100 = now
        if speed_kph >= 200 and self.results["100_200"] is None and self.start_time_100 is not None:
            self.results["100_200"] = now - self.start_time_100
        self.results["peak_torque"] = max(self.results["peak_torque"], torque_nm)
        self.results["peak_power"] = max(self.results["peak_power"], power_kw)
        self.results["g_force_max"] = max(self.results["g_force_max"], g_force)
        self.ui.update(speed_kph, g_force, power_kw, torque_nm,
                       self.results["0_60"], self.results["0_100"], self.results["100_200"])

    def stop(self) -> None:
        if not self.running:
            return
        self.running = False
        video_path = self.recorder.stop()
        self.ui.stop()
        end_time = time.time()
        total_duration = None
        if self.start_time is not None:
            total_duration = end_time - self.start_time
        session = {
            "0_60_kph": self.results["0_60"],
            "0_100_kph": self.results["0_100"],
            "100_200_kph": self.results["100_200"],
            "peak_torque_nm": self.results["peak_torque"],
            "peak_power_kw": self.results["peak_power"],
            "g_force_max": self.results["g_force_max"],
            "total_duration_s": total_duration,
            "video": video_path,
        }
        os.makedirs("/data/sdracemode/sessions", exist_ok=True)
        ts = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        session_file = f"/data/sdracemode/sessions/{ts}.json"
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(session, f, indent=2)
