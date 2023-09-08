import os
import librosa
import soundfile as sf
from joblib import Parallel, delayed
from tqdm import tqdm
import subprocess
# Source directory containing subdirectories
source_directory = '/srv/nas_data1/speech/tts/other_datasets/medium_partitioned/'

def upsample_audio(input_file, output_file, target_sample_rate):
    # Construct the sox command
    cmd = [
        "sox",
        input_file,
        "-r", str(target_sample_rate),
        output_file
    ]
    # Run the sox command
    try:
        subprocess.run(cmd, check=True)
        print(f"Upsampling complete. Output saved as {output_file}")
    except subprocess.CalledProcessError:
        print("Error during upsampling.")

def find_wav_files(root_dir):
    wav_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.wav') and not("upsampled" in filename):
                full_path = os.path.join(dirpath, filename)
                wav_files.append((os.path.splitext(filename)[0], full_path))
    
    return wav_files
# Target sample rate for upsampling
target_sample_rate = 24000
wavs = find_wav_files(source_directory)
wavs = [item[1] for item in wavs]
wavs.sort()
print(len(wavs))

def upsample(wav_file):
    out_filename = os.path.basename(wav_file)
    out_dir = os.path.dirname(wav_file)
    output_path = out_dir + "/upsampled_" + out_filename
    if os.path.isfile(output_path):
        return
    audio, _ = librosa.load(wav_file, sr=None)
    upsampled_audio = librosa.resample(audio, orig_sr=len(audio), target_sr=target_sample_rate)
    sf.write(output_path, upsampled_audio, target_sample_rate, subtype='PCM_16')

# Parallel(n_jobs=15)(delayed(upsample)(wav_file) for wav_file in tqdm(wavs, desc="Processing"))

for item in wavs:
    print(item)
    out_filename = os.path.basename(item)
    out_dir = os.path.dirname(item)
    output_path = out_dir + "/upsampled_" + out_filename
    upsample_audio(item, output_path, target_sample_rate)
