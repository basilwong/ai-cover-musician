"""
Creates the final version of the mp3 using the output of the main.ipynb
notebook.


"""


import os
import pydub
import json
from tqdm import tqdm

# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append('src')

import audio_util
import processing_util

POLLY_OUTPUT_FOLDER = "polly-output/"
BACKGROUND_FOLDER = "source-separation-output/background/"
FINAL_OUTPUT_FOLDER = "final-output/"
SONG_TRANSCRIPTION_PATH = "song-transcription/transcribed_song.json"
BATCH_LENGTH = 30000 # m

# Generate Background
print("Generating the accompaniment...")
background_mp3_files = [BACKGROUND_FOLDER + s for s in sorted(os.listdir(BACKGROUND_FOLDER))]
background_mp3 = audio_util.interpret_polly_output_file(background_mp3_files[0])
background_mp3_files.pop(0)
for fname in tqdm(background_mp3_files):
    background_mp3 += audio_util.interpret_polly_output_file(fname)
background_mp3.export(FINAL_OUTPUT_FOLDER + "background.mp3", format="mp3")

# Generate Vocals
print("Generating the vocals...")
polly_output = sorted(os.listdir(POLLY_OUTPUT_FOLDER))
song_transcription = json.load(open(SONG_TRANSCRIPTION_PATH, "r", encoding="utf-8"))

vocal_mp3 = audio_util.get_silence(1)
expected_start_time = 0

for transcription_item, mp3_file in tqdm(list(zip(song_transcription, polly_output))):
    if expected_start_time < transcription_item["start_time"]:
        vocal_mp3 += audio_util.get_silence(transcription_item["start_time"] - expected_start_time)
        expected_start_time = transcription_item["start_time"]

    assert(mp3_file.startswith(transcription_item["index"]))
    audio_clip = audio_util.interpret_polly_output_file(POLLY_OUTPUT_FOLDER + mp3_file)

# Version 1.1
    vocal_mp3 += audio_clip
    expected_start_time += len(audio_clip)
# Version 2.1
    # corrected_audio_clip = None
    # if transcription_item["end_time"] - transcription_item["start_time"] > 50:
    #     corrected_audio_clip = audio_util.pitch_correction(audio_clip, transcription_item["start_time"], transcription_item["end_time"], "temp/")
    # if corrected_audio_clip:
    #     vocal_mp3 += corrected_audio_clip
    #     expected_start_time += len(corrected_audio_clip)
    # else:
    #     vocal_mp3 += audio_clip
    #     expected_start_time += len(audio_clip)

vocal_mp3.export(FINAL_OUTPUT_FOLDER + "vocals.mp3", format="mp3")


print("Overlaying the vocals with the accompaniment and generating the final audio file...")
final_audio = background_mp3.overlay(vocal_mp3)
final_audio.export(FINAL_OUTPUT_FOLDER + "final_audio.mp3", format="mp3")
print("Done.")
