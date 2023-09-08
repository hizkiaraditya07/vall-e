from lhotse import RecordingSet, Recording
import os
import librosa
import argparse
from pathlib import Path
import logging

def find_wav_files(root_dir):
    wav_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.wav') and not("original" in filename):
                full_path = os.path.join(dirpath, filename)
                wav_files.append((os.path.splitext(filename)[0], full_path))
    print(type(wav_files))
    return wav_files

def check_audio_gt_duration(audio, duration):
    audio_data, sampling_rate = librosa.load(audio, sr=None, mono=False)
    audio_duration = librosa.get_duration(y=audio_data, sr=sampling_rate)

    return audio_duration > duration

root = "/srv/nas_data1/speech/tts/other_datasets/medium_partitioned/"
wav_files = find_wav_files(root)
wav_files = [item[1] for item in wav_files]
wav_files.sort()
wav_files = [item for item in wav_files if not(check_audio_gt_duration(item, 1000))]
print(len(wav_files))

recs = RecordingSet.from_recordings(Recording.from_file(p) for p in wav_files)
recs.to_file(f'./librilight_recordings_all.jsonl.gz')