def run_autoconfig():
  # Read car data; here simplified (replace with real carParams)
  is_ev = True
  flags = {
    "SDR_EV": "1" if is_ev else "0",
    "SDR_DualMotor": "1",
    "SDR_HasDrift": "1" if is_ev else "0",
    "SDR_HasTorqueSplit": "1" if is_ev else "0",
    "SDR_HasFrontMotorControl": "1" if is_ev else "0",
    "SDR_Unit": "kW" if is_ev else "HP"
  }
  try:
    from openpilot.common.params import Params
    p=Params()
    for k,v in flags.items(): p.put(k,v)
  except Exception:
    pass
  return flags
