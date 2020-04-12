import wave
import contextlib

def get_audio_duration_wav(fname):
    """
    Takes a string specifying the path to a .wav file and returns the duration
    of the audio file in seconds.
    """
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)
