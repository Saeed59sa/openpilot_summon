"""SDRaceMode disclaimer screen."""
from __future__ import annotations
from common.params import Params

def ensure_disclaimer() -> bool:
    """Show disclaimer text on first run and require acceptance."""
    params = Params()
    if params.get_bool("SDRaceModeAccepted"):
        return True
    # In the real system this would display a full screen dialog. Here we simply
    # log the message and assume acceptance for demonstration purposes.
    disclaimer = (
        "SDRaceMode – Terms of Use\n\n"
        "By using SDRaceMode, you confirm that:\n"
        "• You will only use it in private or legal areas (e.g., race tracks)\n"
        "• You accept full responsibility for any outcomes\n"
        "• You understand this mode may disable vehicle safety features\n"
        "• You acknowledge it is illegal to use on public roads\n"
    )
    print(disclaimer)
    params.put("SDRaceModeAccepted", "1")
    return True
