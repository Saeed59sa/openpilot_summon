"""EV specific control helpers for SDRaceMode."""
from __future__ import annotations
from common.params import Params


class EVController:
    """Simple parameter based EV control implementation."""
    def __init__(self) -> None:
        self.params = Params()

    def apply_settings(self) -> None:
        """Send settings to the car via Params for external processes to consume."""
        settings = {
            "drift_mode": self.params.get_bool("SDRM_DriftMode"),
            "torque_split": self.params.get("SDRM_TorqueSplit") or "0:100",
            "disable_front_motor": self.params.get_bool("SDRM_DisableFrontMotor"),
            "disable_traction_control": self.params.get_bool("SDRM_DisableTraction"),
        }
        self.params.put("SDRaceModeEVSettings", str(settings))
