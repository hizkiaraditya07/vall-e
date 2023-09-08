import whisper
import os

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
root_directory = "./medium/"
wav_files_found = find_wav_files(root_directory)
print(len(wav_files_found))
counter = 0

for wav_file in wav_files_found:
    counter += 1
    wav_name = wav_file[1]
    txt_name = "." + wav_file[1].split(".")[1] + ".txt"
    print(counter)
    print(txt_name)
    if os.path.exists(txt_name):
        print("yes")
    # result = model.transcribe(wav_name)
    # text = result["text"]
    # with open(txt_name, 'w') as file:
    #     file.write(text)
