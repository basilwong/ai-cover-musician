import processing_util
from pydub import AudioSegment
import os, shutil
import json
from scipy.io import wavfile
import crepe
import numpy as np
from math import log2, pow

A4 = 440
C0 = A4*pow(2, -4.75)

def freq_to_pitch(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return octave*12 + n

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
    processing_util.clear_folder(output_path)
    while total_duration < len(sound):
        if total_duration + THIRTY_SEC > len(sound):
            new_file = sound[total_duration:]
        else:
            new_file = sound[total_duration:total_duration+THIRTY_SEC]
        new_file.export(output_path + "input" + str(num_files) + ".mp3", format="mp3")

        total_duration += THIRTY_SEC
        num_files += 1

def get_silence(duration):
    """
    Assumes called from main.ipynb

    duration is in milliseconds
    """
    sound = AudioSegment.from_mp3("src/silence.mp3")
    return sound[:duration]

def determine_pitch(audio_segment, temp_folder):
    if len(audio_segment) < 10:
        return None
    temp_path = temp_folder + "file.wav"
    audio_segment.export(temp_path, format="wav")
    sr, audio = wavfile.read(temp_path)
    time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)
    return freq_to_pitch(np.average(frequency))

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

def speedx(sound_array, factor):
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int) ]

def stretch(sound_array, f, window_size, h):
    """ Stretches the sound by a factor `f` """

    phase  = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros( len(sound_array) /f + window_size)

    for i in np.arange(0, len(sound_array)-(window_size+h), h*f):

        # two potentially overlapping subarrays
        a1 = sound_array[i: i + window_size]
        a2 = sound_array[i + h: i + window_size + h]

        # resynchronize the second array on the first
        s1 =  np.fft.fft(hanning_window * a1)
        s2 =  np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2/s1)) % 2*np.pi
        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))

        # add to result
        i2 = int(i/f)
        result[i2 : i2 + window_size] += hanning_window*a2_rephased

    result = ((2**(16-4)) * result/result.max()) # normalize (16bit)

    return result.astype('int16')

def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)

def shift_audio_pitch(audio_segment, n, temp_folder):
    temp_path = temp_folder + "file.wav"
    audio_segment.export(temp_path, format="wav")
    sr, audio = wavfile.read(temp_path)
    factor = 2**(1.0 * n / 12.0)
    # TODO: make remove the truncation
    audio_shifted = speedx(audio, factor) # not shifted
    wavfile.write(temp_path, sr, audio_shifted)
    if audio_shifted.size == 0:
        return None
    return AudioSegment.from_wav(temp_path)

def get_original_sample(start_time, end_time):
    BATCH_SIZE = 30000
    VOCALS_FOLDER = "source-separation-output/vocals/"
    batch = str(int(start_time // BATCH_SIZE)).zfill(5)
    for file in os.listdir(VOCALS_FOLDER):
        if batch in file:
            fname = file
            break
    return AudioSegment.from_wav(VOCALS_FOLDER + fname)[start_time%BATCH_SIZE:end_time%BATCH_SIZE]

def pitch_correction(audio_segment, start_time, end_time, temp_folder):
    pitch1 = determine_pitch(audio_segment, temp_folder)
    pitch2 = determine_pitch(get_original_sample(start_time, end_time), temp_folder)
    if pitch1 is None or pitch2 is None:
        return None
    n = pitch2 - pitch1
    return shift_audio_pitch(audio_segment, n, temp_folder)

if __name__ == "__main__":
    split_mp3("../archive/songs/bmjtwya_song3.mp3", "../source-separation-input/just_the_way_you_are-bruno_mars/")
    # print(determine_pitch(interpret_polly_output_file("test.mp3"), "../temp/"))
