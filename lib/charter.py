from lib.audio import get_metronome_ticks
from lib.bpm import calculate_bpm, calculate_bpm_compass
from typing import List, Dict, Final
from numpy import float64
from model.chart import Chart
from lib.constants import UPLOADS_PATH

INITIAL_TIME: Final[int] = 0
INITIAL_TICK: Final[int] = 0
INITIAL_BPM: Final[int] = 120
CHART_FILE_NAME: Final[str] = "notes.chart"

def generate_chart(audio_path: str, chart: Chart) -> None:

    print(f"[{chart.id}] Loading audio...")
    times = get_metronome_ticks(audio_path)
    if chart.skip > 0:
        print(f"[{chart.id}] Skipping beats...")
        times = times[chart.skip:]
    print(f"[{chart.id}] Syncing track...")
    track = sync_track(times)
    print(f"[{chart.id}] Generating chart file...")
    chart_content = generate_chart_content(track, chart)
    write_chart_file(chart_content, chart.id)

def sync_track(times: List[float64]) -> List[Dict]:
    track: List[Dict] = []
    
    prev_time = INITIAL_TIME
    current_tick = INITIAL_TICK
    current_bpm = INITIAL_BPM

    for current_time in times:
        if prev_time == INITIAL_TIME:
            data = calculate_bpm_compass(current_bpm, current_time)
        else:
            data = calculate_bpm(current_bpm, current_tick, prev_time, current_time)
        
        if (data["next_bpm"] == 0):
            continue
        
        track.append(data)

        current_bpm = data["next_bpm"]
        current_tick = data["next_tick"]
        prev_time = current_time
    
    return track

def generate_chart_content(track: List[Dict], chart: Chart) -> str:
    chart_content = """[Song]
{
  Name = """ + chart.song + """
  Artist = """ + chart.artist + """
  Charter = """ + chart.charter + """
  Offset = 0
  Resolution = 192
  Player2 = bass
  Difficulty = 0
  PreviewStart = 0
  PreviewEnd = 0
  Genre = ""
  MediaType = "cd"
}
[SyncTrack]
{
  0 = TS 4\n"""

    for data in track:
        chart_content += f"  {int(data["current_tick"])} = B {int(data["next_bpm"] * 1000)}\n"
    
    chart_content += """}
[Events]
{
}
"""

    return chart_content

def write_chart_file(chart_content: str, id: str) -> None:
    with open(f"{UPLOADS_PATH}/{id}-{CHART_FILE_NAME}", "w") as f:
        f.write(chart_content)