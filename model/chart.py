from typing import NamedTuple
from werkzeug.datastructures import FileStorage


class Chart(NamedTuple):
    id: str
    file: FileStorage
    song: str
    artist: str
    charter: str
    skip: int