from librosa import load, feature, amplitude_to_db, frames_to_time
from numpy import where, max, float64
from typing import List, Final

THRESHOLD: Final[int] = -5

def get_metronome_ticks(path: str) -> List[float64]:
    y, sr = load(path, sr=None)
    rms = feature.rms(y=y)[0]
    rms_db = amplitude_to_db(rms, ref=max)
    indexes = where(rms_db > THRESHOLD)[0]
    times = frames_to_time(indexes, sr=sr)
    return filter_times(list(map(lambda x: round(x, 2), times)))

def filter_times(times: List[float64]) -> List[float64]:
    stack: List[float64] = []

    for time in times:
        if len(stack) == 0:
            stack.append(time)
        elif (time - stack[-1]) > 0.1:
            stack.append(time)

    return stack

    