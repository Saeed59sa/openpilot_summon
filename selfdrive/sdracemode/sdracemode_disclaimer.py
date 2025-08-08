from __future__ import annotations

from common.params import Params

DISCLAIMER = (
  "\n\n\u26d6 SDRaceMode – Terms of Use\n"
  "\u2022 Use only in private, legal, or track environments\n"
  "\u2022 You accept full responsibility for activation\n"
  "\u2022 SDRaceMode may disable traction/safety systems\n"
  "\u2022 It is illegal to use this feature on public roads\n\n"
  "[y] Accept and Enable   [n] Cancel\n"
)


def check_disclaimer(params: Params | None = None) -> bool:
  """Show the disclaimer if it has not been accepted."""
  p = params or Params()
  if p.get("SDRaceModeAccepted") == "1":
    return True

  try:
    # In a real system this would be a full screen UI. For this module we
    # simply print to the console and require an explicit confirmation.
    choice = input(DISCLAIMER)
  except EOFError:
    choice = "n"

  if choice.lower().startswith("y"):
    p.put("SDRaceModeAccepted", "1")
    return True
  return False
