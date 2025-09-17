from model.chart import Chart
from exception.validation import ValidationException

def validate_chart(chart: Chart) -> None:
    if not chart.file:
        raise ValidationException("MISSING_METRONOME")

    if chart.file.mimetype != "audio/mpeg":
        raise ValidationException("UNSUPPORTED_METRONOME")
    
    if not chart.charter:
        raise ValidationException("MISSING_CHARTER")
        
    if not chart.song:
        raise ValidationException("MISSING_SONG")

    if not chart.artist:
        raise ValidationException("MISSING_ARTIST")
    
    if chart.skip < 0:
        raise ValidationException("UNSUPPORTED_SKIP")