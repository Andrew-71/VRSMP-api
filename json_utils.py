import json

def write_to_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def read_from_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)