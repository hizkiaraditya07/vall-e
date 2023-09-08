import gzip
import json

file_path = './data/manifests/librilight_supervisions_all.jsonl.gz'

# Open the file in binary mode ('rb') and decompress it using gzip.
with gzip.open(file_path, 'rb') as f:
    # Iterate through each line in the decompressed file.
    for line in f:
        # Convert the line (which is a bytes object) to a string.
        line_str = line.decode('utf-8')
        # Parse the JSON object from the string and process it as needed.
        data = json.loads(line_str)
        # Do something with the JSON object, e.g., print it.
        print(data)
        break
        