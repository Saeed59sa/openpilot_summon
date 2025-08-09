def ensure_disclaimer_accepted():
  # NOTE: replace with real UI modal; here we simulate stored consent via Params if available
  try:
    from openpilot.common.params import Params
    p=Params()
    if p.get("SDRaceModeAccepted")==b"1": return True
    # In real UI: show dialog. Here we auto-accept for scaffolding.
    p.put("SDRaceModeAccepted","1")
    return True
  except Exception:
    return True
