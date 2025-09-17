from flask import Flask, request, jsonify
import uuid

from lib.charter import generate_chart
from model.chart import Chart
from service.validate_chart import validate_chart
from service.save_tmp import save_tmp_file
from exception.validation import ValidationException
from lib.constants import MAX_BPM_FILE_SIZE
from service.clear_cache import clear_cache

app = Flask(__name__)

app.config["MAX_CONTENT_LENGH"] = MAX_BPM_FILE_SIZE

@app.route("/charts", methods = ["POST"])
def create_chart():
    id = str(uuid.uuid4())
    file = request.files.get("metronome")
    charter = request.form.get("charter")
    song = request.form.get("song")
    artist = request.form.get("artist")
    skip = request.form.get("skip") or 0

    chart = Chart(id = id, file=file, song=song, artist=artist, charter=charter, skip=skip)

    response = {}
    code = 200

    try:
        validate_chart(chart)
        path = save_tmp_file(file, id)
        generate_chart(audio_path=path, chart=chart)

        response = {
            "id": id
        }
    except ValidationException as err:
        response= {
            "error": True,
            "code": err.code,
            "message": "Request is invalid"
        }

        code = 422
    except Exception as err:
        response = {
            "error": True,
            "code": "UNKNOWN_ERROR",
            "message": err.args
        }
        code = 500
    finally:
        clear_cache(id)
        return jsonify(response), code
    
    

@app.errorhandler(413)
def request_entity_too_large():
    return jsonify({
        "error": True,
        "code": "BPM_TOO_LARGE"
    })