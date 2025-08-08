"""User interface elements for SDRaceMode."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class HUDData:
    speed: float = 0.0
    g_force: float = 0.0
    power: float = 0.0
    torque: float = 0.0
    timer_0_60: Optional[float] = None
    timer_0_100: Optional[float] = None
    timer_100_200: Optional[float] = None


class SDRaceModeUI:
    """Placeholder HUD overlay implementation."""
    def __init__(self) -> None:
        self.hud_data = HUDData()
        self.active = False

    def start(self) -> None:
        self.active = True

    def update(self, speed: float, g_force: float, power: float, torque: float,
               timer_0_60: Optional[float], timer_0_100: Optional[float],
               timer_100_200: Optional[float]) -> None:
        if not self.active:
            return
        self.hud_data.speed = speed
        self.hud_data.g_force = g_force
        self.hud_data.power = power
        self.hud_data.torque = torque
        self.hud_data.timer_0_60 = timer_0_60
        self.hud_data.timer_0_100 = timer_0_100
        self.hud_data.timer_100_200 = timer_100_200

    def stop(self) -> None:
        self.active = False
