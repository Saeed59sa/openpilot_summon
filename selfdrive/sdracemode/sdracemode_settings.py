"""Settings management for SDRaceMode."""
from __future__ import annotations
from dataclasses import dataclass
from common.params import Params


@dataclass
class SDRaceModeSettings:
    enable: bool = False
    power_unit: str = "HP"
    record_audio: bool = True
    video_quality: str = "High"
    auto_start: bool = False
    show_g_force: bool = True
    drift_mode: bool = False
    torque_split: str = "50:50"
    disable_front_motor: bool = False
    disable_traction: bool = False


class SettingsManager:
    """Persist settings via Params."""
    def __init__(self) -> None:
        self.params = Params()

    def load(self) -> SDRaceModeSettings:
        p = self.params
        return SDRaceModeSettings(
            enable=p.get_bool("SDRM_Enable"),
            power_unit=p.get("SDRM_PowerUnit") or "HP",
            record_audio=p.get_bool("SDRM_RecordAudio"),
            video_quality=p.get("SDRM_VideoQuality") or "High",
            auto_start=p.get_bool("SDRM_AutoStart"),
            show_g_force=p.get_bool("SDRM_ShowGForce"),
            drift_mode=p.get_bool("SDRM_DriftMode"),
            torque_split=p.get("SDRM_TorqueSplit") or "50:50",
            disable_front_motor=p.get_bool("SDRM_DisableFrontMotor"),
            disable_traction=p.get_bool("SDRM_DisableTraction"),
        )

    def save(self, settings: SDRaceModeSettings) -> None:
        p = self.params
        p.put_bool("SDRM_Enable", settings.enable)
        p.put("SDRM_PowerUnit", settings.power_unit)
        p.put_bool("SDRM_RecordAudio", settings.record_audio)
        p.put("SDRM_VideoQuality", settings.video_quality)
        p.put_bool("SDRM_AutoStart", settings.auto_start)
        p.put_bool("SDRM_ShowGForce", settings.show_g_force)
        p.put_bool("SDRM_DriftMode", settings.drift_mode)
        p.put("SDRM_TorqueSplit", settings.torque_split)
        p.put_bool("SDRM_DisableFrontMotor", settings.disable_front_motor)
        p.put_bool("SDRM_DisableTraction", settings.disable_traction)
