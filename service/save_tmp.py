from werkzeug.datastructures import FileStorage

def save_tmp_file(file: FileStorage, id: str) -> str:
    path = f"/tmp/{id}-metronome.mp3"
    file.save(path)
    return path