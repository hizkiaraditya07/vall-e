import os
import subprocess

def convert_flac_to_wav(input_file, output_file):
    subprocess.run(["sox", input_file, output_file])

def find_flac_files(directory):
    flac_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".flac"):
                flac_files.append(os.path.join(root, file))
    return flac_files

def convert_all_flac_to_wav(directory):
    flac_files = find_flac_files(directory)
    for flac_file in flac_files:
        print(flac_file)
        wav_file = os.path.splitext(flac_file)[0] + ".wav"
        convert_flac_to_wav(flac_file, wav_file)

# Replace 'your_directory_path' with the actual path of the directory you want to search
directory_path = '/srv/nas_data1/speech/tts/other_datasets/medium_partitioned/'
convert_all_flac_to_wav(directory_path)