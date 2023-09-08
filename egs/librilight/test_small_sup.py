import librosa
from lhotse import SupervisionSet, SupervisionSegment
import os
import argparse
from pathlib import Path
import logging

def find_txt_files(root_dir):
    txt_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.txt'):
                full_path = os.path.join(dirpath, filename)
                txt_files.append((os.path.splitext(filename)[0], full_path))
    
    return txt_files

def find_wav_files(root_dir):
    wav_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.wav') and not("original" in filename):
                full_path = os.path.join(dirpath, filename)
                wav_files.append((os.path.splitext(filename)[0], full_path))
    print(type(wav_files))
    return wav_files

root = "/srv/nas_data1/speech/tts/other_datasets/medium_preprocessed"
wav_files = find_wav_files(root)
wav_files = [item[1] for item in wav_files]
wav_files.sort()

root = "/srv/nas_data1/speech/tts/other_datasets/medium_preprocessed"
txt_files = find_txt_files(root)
txt_files = [item[1] for item in txt_files]
txt_files.sort()

supervisionset= []
i = 0
for wav, text in zip(wav_files, txt_files):
    with open(text, 'r') as f:
        ntext = f.read()

    base_name = os.path.basename(text)
    fname = os.path.splitext(base_name)[0]

    audio_data, sampling_rate = librosa.load(wav, sr=None, mono=False)
    audio_duration = librosa.get_duration(y=audio_data, sr=sampling_rate)
    
    customd = {"orig_text" : ntext}

    new_supervision = SupervisionSegment(id=fname, recording_id=fname, start=0.0, 
                                            duration=audio_duration, text=ntext, channel=0, custom=customd)
        
    supervisionset.append(new_supervision)    

sup = SupervisionSet.from_segments(supervisionset)
sup.to_file(f'librilight_supervisions_all.jsonl.gz')