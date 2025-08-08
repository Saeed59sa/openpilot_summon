from __future__ import annotations

import json
from typing import Dict, Any

from common.params import Params


class SDRAutoConfig:
  """Auto configuration logic for SDRaceMode.

  The module reads basic car parameters and fingerprint data to enable or
  disable features dynamically.  All decisions are stored in :class:`Params`
  so other modules can read the configuration without recomputing it.
  """

  def __init__(self, params: Params | None = None) -> None:
    self.params = params or Params()

  def configure(self, car_params: Dict[str, Any], fingerprint: str) -> Dict[str, Any]:
    """Run auto configuration.

    Parameters
    ----------
    car_params: dict
      Dictionary with car characteristics.  Only a minimal subset is
      required: ``fuelType`` (``"electric"`` for EVs) and ``dualMotor``.
    fingerprint: str
      Unique fingerprint string of the vehicle.

    Returns
    -------
    dict
      Summary of the detected configuration.
    """
    ev = car_params.get("fuelType", "").lower() == "electric"
    dual_motor = bool(car_params.get("dualMotor", False))

    self.params.put("SDR_EV", "1" if ev else "0")
    self.params.put("SDR_DualMotor", "1" if dual_motor else "0")

    unit = "kW" if ev else "HP"
    self.params.put("SDR_Unit", unit)

    has_drift = "1" if ev else "0"
    has_torque_split = "1" if dual_motor else "0"
    has_front_motor = "1" if ev and dual_motor else "0"

    self.params.put("SDR_HasDrift", has_drift)
    self.params.put("SDR_HasTorqueSplit", has_torque_split)
    self.params.put("SDR_HasFrontMotorControl", has_front_motor)

    config = {
      "fingerprint": fingerprint,
      "ev": ev,
      "dual_motor": dual_motor,
      "unit": unit,
    }
    self.params.put("SDR_LastAutoConfig", json.dumps(config))
    return config
