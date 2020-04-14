import wave
import contextlib
from pydub import AudioSegment
import os, shutil
import json

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

def split_mp3(fname, output_path):
    """
    Takes a string specifying the path to an .mp3 file.
    Splits the file into 30 second segments.
    Writes all 30 second length audio files in the given folder path output_path.
    """
    THIRTY_SEC = 30000 # in milliseconds
    sound = AudioSegment.from_mp3(fname)
    total_duration = 0
    num_files = 1
    # Clear the output folder.
    clear_folder(output_path)
    while total_duration < len(sound):
        if total_duration + THIRTY_SEC > len(sound):
            new_file = sound[total_duration:]
        else:
            new_file = sound[total_duration:total_duration+THIRTY_SEC]
        new_file.export(output_path + "input" + str(num_files) + ".mp3", format="mp3")

        total_duration += THIRTY_SEC
        num_files += 1

def get_audio_duration_wav(fname):
    """
    Takes a string specifying the path to a .wav file and returns the duration
    of the audio file in seconds.
    """
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)

def get_silence(duration):
    """
    Assumes called from main.ipynb

    duration is in milliseconds
    """
    sound = AudioSegment.from_mp3("src/silence.mp3")
    return sound[:duration]

def determine_pitch(fname):
    pass
    # TODO

def interpret_polly_output_file(fname):
    """
    If the file is a json file it means it represents a gap in singing/rapping.
    Thus, returns an pydub interpreted mp3 silent mp3.

    Otherwise the file is an mp3 and is returned as pydub interpretted mp3.
    """
    if fname.endswith(".json"):
        data = json.load(open(fname, "r", encoding="utf-8"))
        return get_silence(data["length"])
    elif fname.endswith(".mp3"):
        return AudioSegment.from_mp3(fname)
    elif fname.endswith(".wav"):
        return AudioSegment.from_wav(fname)
    else:
        raise Exception('Unknown file in the polly output folder: ' + fname)

if __name__ == "__main__":
    split_mp3("../songs/drake-toosie_slide.mp3", "../source-separation-input/")
