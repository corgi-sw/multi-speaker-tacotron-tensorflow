import os
import re
import sys
import json
import argparse
import numpy as np
from tqdm import tqdm
from glob import glob
from pydub import silence
from pydub import AudioSegment
from functools import partial

from hparams import hparams
from utils import parallel_run, add_postfix
from audio import load_audio, save_audio, get_duration, get_silence

def read_audio(audio_path):
    return AudioSegment.from_file(audio_path)

def split_on_silence_with_pydub(
        audio_path, skip_idx=0, out_ext="wav",
        silence_thresh=-40, min_silence_len=4900,
        silence_chunk_len=100, keep_silence=100):

    filename = os.path.basename(audio_path).split('.', 1)[0]
    in_ext = audio_path.rsplit(".")[1]

    audio = read_audio(audio_path)
    not_silence_ranges = silence.detect_nonsilent(
        audio, min_silence_len=silence_chunk_len,
        silence_thresh=silence_thresh)

    edges = [not_silence_ranges[0]]

    for idx in range(1, len(not_silence_ranges)-1):
        cur_start = not_silence_ranges[idx][0]
        prev_end = edges[-1][1]

        if cur_start - prev_end < min_silence_len:
            edges[-1][1] = not_silence_ranges[idx][1]
        else:
            edges.append(not_silence_ranges[idx])
    
    audio_paths = []
    file_number = 0
    for idx, (start_idx, end_idx) in enumerate(edges[skip_idx:]):
        start_idx = max(0, start_idx - keep_silence)
        end_idx += keep_silence + 200

        target_audio_path = "{}/{}.{:04d}.{}".format(
            os.path.dirname(audio_path), filename, file_number, out_ext)

        audio_length_ms = end_idx-start_idx
        if (audio_length_ms < 500):
            print("X", target_audio_path, audio_length_ms)

        else:
            segment=audio[start_idx:end_idx]
            segment.export(target_audio_path, out_ext) 
        
            audio_paths.append(target_audio_path)
            file_number += 1

            print("O", target_audio_path, audio_length_ms)

    return audio_paths

def combine_split(path):
    raw_audio_dir = path + '/raw_audio/'
    combined_audio_dir = path + '/audio/'

    silence_audio_5_path = './audio/silence_5.wav'
    silence_audio_5 = AudioSegment.from_wav(silence_audio_5_path)

    arr_raw_audio = glob("{}/*.wav".format(raw_audio_dir))
    arr_raw_audio = sorted(arr_raw_audio)

    idx = 0
    combined_audio = silence_audio_5
    for raw_audio_path in arr_raw_audio:
        raw_audio = AudioSegment.from_file(raw_audio_path)
        combined_audio += raw_audio + silence_audio_5
        print(idx)
        idx += 1

    # dummy
    combined_audio += AudioSegment.from_wav('./audio/dummy.wav')
    # dummy

    combined_audio_path = combined_audio_dir + 'Raw.wav'
    combined_audio.export(combined_audio_path, format='wav')

    r = split_on_silence_with_pydub(combined_audio_path, min_silence_len=4900)

def combine(path):
    raw_audio_dir = path + '/raw_audio/'
    combined_audio_dir = path + '/combined_audio/'

    silence_audio_0_path = './audio/silence_0.wav'
    silence_audio_0 = AudioSegment.from_wav(silence_audio_0_path)
    silence_audio_2_path = './audio/silence_2.wav'
    silence_audio_2 = AudioSegment.from_wav(silence_audio_2_path)

    arr_raw_audio = glob("{}/*.wav".format(raw_audio_dir))
    arr_raw_audio = sorted(arr_raw_audio)

    print(arr_raw_audio)

    combined_audio = silence_audio_0
    for raw_audio_path in arr_raw_audio:
        raw_audio = AudioSegment.from_wav(raw_audio_path) # from file? from wav?
        combined_audio += raw_audio + silence_audio_2

    combined_audio_path = combined_audio_dir + 'Combined.wav'
    combined_audio.export(combined_audio_path, format='wav')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True)
    config = parser.parse_args()

    # config.path = './datasets/msw'
    
    combine_split(config.path)
    # combine(config.path)