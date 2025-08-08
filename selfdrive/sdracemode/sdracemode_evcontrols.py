from __future__ import annotations

from common.params import Params

from .sdracemode_settings import SDRaceModeSettings


class SDRaceEVControls:
  """Apply EV specific control settings."""

  def __init__(self, settings: SDRaceModeSettings) -> None:
    self.settings = settings
    self.params = Params()

  def apply(self) -> None:
    if self.params.get("SDR_EV") != "1":
      return

    if self.settings.enable_drift:
      self.params.put("SDR_DriftMode", "1")
    else:
      self.params.put("SDR_DriftMode", "0")

    if self.params.get("SDR_HasTorqueSplit") == "1":
      self.params.put("SDR_TorqueSplitCommand", str(self.settings.torque_split))

    if self.settings.disable_front_motor and self.params.get("SDR_HasFrontMotorControl") == "1":
      self.params.put("SDR_FrontMotor", "0")

    if self.settings.disable_traction:
      self.params.put("SDR_TractionControl", "0")
    else:
      self.params.put("SDR_TractionControl", "1")
