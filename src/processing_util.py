import json

def load_json(file):
    """Load in JSON file and return as dict"""

    json_filepath = Path(file)
    assert json_filepath.is_file(), "JSON file does not exist"

    data = json.load(open(json_filepath.absolute(), "r", encoding="utf-8"))
    assert "jobName" in data
    assert "results" in data
    assert "status" in data

    assert data["status"] == "COMPLETED", "JSON file not shown as completed."

    return data

class TranscriptionData:

    def __init__(self, start_time, end_time, confidence, content, type):
        self.start_time = float(start_time)
        self.end_time = float(end_time)
        self.confidence = float(confidence)
        self.content = content
        self.type = type

    def is_word(self):
        return self.type = "pronunciation"

    def duration(self):
        return self.end_time - self.start_time
