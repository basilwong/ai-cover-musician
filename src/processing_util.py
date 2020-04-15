class TranscriptionItem:

    def __init__(self, item_dict, index, offset=0):
        self.index = str(index).zfill(5)
        self.type = item_dict["type"]
        alternatives = item_dict["alternatives"][0]
        self.confidence = float(alternatives["confidence"])
        self.content = alternatives["content"]
        if self.is_word():
            self.start_time = (float(item_dict["start_time"]) * 1000) + offset # milliseconds
            self.end_time = (float(item_dict["end_time"]) * 1000) + offset # milliseconds

    def is_word(self):
        return self.type == "pronunciation"

    def duration(self):
        return self.end_time - self.start_time
    
    def to_dict(self):
        ret = dict()
        ret["index"] = self.index
        ret["content"] = self.content
        ret["start_time"] = self.start_time
        ret["end_time"] = self.end_time
        return ret
