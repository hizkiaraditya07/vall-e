import os

def delete_flac_files(directory):
    for root, subdirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".flac"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")

def main():
    target_directory = "/srv/nas_data1/speech/tts/other_datasets/medium_partitioned/"  # Change this to the directory you want to start from
    delete_flac_files(target_directory)

if __name__ == "__main__":
    main()