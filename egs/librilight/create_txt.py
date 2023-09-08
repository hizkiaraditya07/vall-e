import whisper
import os
from joblib import Parallel, delayed
from tqdm import tqdm

model = whisper.load_model("base")

def find_wav_files(root_dir):
    wav_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.wav'):
                full_path = os.path.join(dirpath, filename)
                wav_files.append((os.path.splitext(filename)[0], full_path))
    
    return wav_files

# Provide the root directory where you want to start searching
root_directory = "/srv/nas_data1/speech/tts/other_datasets/medium_partitioned/"
wav_files_found = find_wav_files(root_directory)
wav_files_found = [item[1] for item in wav_files_found]
print(len(wav_files_found))
print(wav_files_found[1])

def create_txt(wav_file):
    wav_name = wav_file
    base_name = os.path.basename(wav_file) #filename.wav
    fname = os.path.splitext(base_name)[0] #filename
    dirname = os.path.dirname(wav_file) #dir
    txt_name =  dirname + "/" + fname + ".txt"
    if os.path.exists(txt_name):
        return
    result = model.transcribe(wav_name)
    text = result["text"]
    with open(txt_name, 'w') as file:
        file.write(text)

Parallel(n_jobs=18)(delayed(create_txt)(wav_file) for wav_file in tqdm(wav_files_found, desc="Processing"))