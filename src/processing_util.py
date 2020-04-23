import os, shutil

def clear_folder(path_to_folder):
    """
    Deletes all files in the specified folder.
    """
    folder = path_to_folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
def clear_s3_folder(bucket, bucket_client, path_to_folder):
    """
    Deletes all objects in specified folder within s3 bucket. 
    """
    for object_summary in bucket.objects.filter(Prefix=path_to_folder):
        bucket_client.delete_object(Bucket=bucket.name, Key=object_summary.key)

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
