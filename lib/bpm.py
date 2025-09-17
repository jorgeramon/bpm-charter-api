from numpy import float64
from typing import Final, Dict

COMPASS: Final[int] = 4
BEAT_TICKS: Final[int] = 192

def calculate_bpm(base_bpm: float, base_tick: int, prev_time: float64, current_time: float64) -> Dict:
    diff_time = current_time - prev_time
    beat_seconds = 60 / base_bpm
    beats = diff_time / beat_seconds
    nearest_beat = round(beats)
    next_tick = (nearest_beat * BEAT_TICKS) + base_tick
    bpm = round((nearest_beat * 60) / diff_time, 2)
    return {
        "current_tick": base_tick,
        "current_bpm": base_bpm,
        "next_tick": next_tick,
        "next_bpm": bpm.item()
    }

def calculate_bpm_compass(base_bpm: float, time: float64) -> Dict:
    beat_seconds = 60 / base_bpm
    beats = time / beat_seconds
    nearest_beat = round(beats / 4) * 4
    next_tick = nearest_beat * BEAT_TICKS
    bpm = round((nearest_beat * 60) / time, 2)
    return {
        "current_tick": 0,
        "current_bpm": base_bpm,
        "next_tick": next_tick,
        "next_bpm": bpm.item()
    }