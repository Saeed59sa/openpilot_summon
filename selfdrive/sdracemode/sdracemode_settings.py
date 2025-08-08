from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from common.params import Params


@dataclass
class SDRaceModeSettings:
  """Store and retrieve SDRaceMode settings using :class:`Params`."""

  params: Params

  DEFAULTS: Dict[str, Any] = None

  def __post_init__(self) -> None:
    if self.DEFAULTS is None:
      self.DEFAULTS = {
        "SDR_Enabled": "0",
        "SDR_VideoQuality": "medium",
        "SDR_RecordAudio": "auto",
        "SDR_AutoStart": "0",
        "SDR_ShowGForce": "1",
        "SDR_EnableDrift": "0",
        "SDR_TorqueSplit": "50",
        "SDR_DisableFrontMotor": "0",
        "SDR_DisableTraction": "0",
      }
    self._ensure_defaults()

  def _ensure_defaults(self) -> None:
    for key, value in self.DEFAULTS.items():
      if self.params.get(key) is None:
        self.params.put(key, str(value))

  # Convenience properties
  @property
  def enabled(self) -> bool:
    return self.params.get("SDR_Enabled") == "1"

  @enabled.setter
  def enabled(self, value: bool) -> None:
    self.params.put("SDR_Enabled", "1" if value else "0")

  @property
  def power_unit(self) -> str:
    unit = self.params.get("SDR_Unit")
    return unit.decode() if isinstance(unit, bytes) else unit or "kW"

  @property
  def record_audio(self) -> bool:
    val = self.params.get("SDR_RecordAudio")
    return (val or "auto").decode() if isinstance(val, bytes) else (val or "auto")

  @property
  def enable_drift(self) -> bool:
    return self.params.get("SDR_EnableDrift") == "1"

  @property
  def torque_split(self) -> int:
    val = self.params.get("SDR_TorqueSplit") or b"50"
    if isinstance(val, bytes):
      val = val.decode()
    return int(val)

  @property
  def disable_front_motor(self) -> bool:
    return self.params.get("SDR_DisableFrontMotor") == "1"

  @property
  def disable_traction(self) -> bool:
    return self.params.get("SDR_DisableTraction") == "1"
