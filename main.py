"""
Creates the final version of the mp3 using the output of the main.ipynb
notebook.
"""


import os
import pydub
from tqdm import tqdm

# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append('src')

import audio_util

POLLY_OUTPUT_FOLDER = "polly-output/"
BACKGROUND_FOLDER = "source-separation-output/background/"
FINAL_OUTPUT_FOLDER = "final-output/"

# Generate Background
background_mp3_files = [BACKGROUND_FOLDER + s for s in sorted(os.listdir(BACKGROUND_FOLDER))]
background_mp3 = audio_util.interpret_polly_output_file(background_mp3_files[0])
background_mp3_files.pop(0)
for fname in tqdm(background_mp3_files):
    background_mp3 += audio_util.interpret_polly_output_file(fname)
background_mp3.export(FINAL_OUTPUT_FOLDER + "background.mp3", format="mp3")

list_of_polly_output = [POLLY_OUTPUT_FOLDER + s for s in sorted(os.listdir(POLLY_OUTPUT_FOLDER))]
vocal_mp3 = audio_util.interpret_polly_output_file(list_of_polly_output[0])
list_of_polly_output.pop(0)
for fname in tqdm(list_of_polly_output):
    vocal_mp3 += audio_util.interpret_polly_output_file(fname)
vocal_mp3.export(FINAL_OUTPUT_FOLDER + "vocals.mp3", format="mp3")

final_audio = background_mp3.overlay(vocal_mp3)

final_audio.export(FINAL_OUTPUT_FOLDER + "final_audio.mp3", format="mp3")
    
#     # Create pause if there is a larger than 1 second gap between words.
#     if expected_start_time + add_pause_for_gaps_greater_than < transcribe_object.start_time:
#         silence_dict["length"] = transcribe_object.start_time - expected_start_time
#         with open(polly_output_folder + str(index).zfill(5) + ".json", 'w') as outfile:
#             json.dump(silence_dict, outfile)
#         expected_start_time = transcribe_object.start_time