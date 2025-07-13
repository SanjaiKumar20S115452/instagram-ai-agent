import json

def load_memes(json_path='memes.json'):
    with open(json_path, 'r') as file:
        return json.load(file)

def get_unposted_memes(all_memes, posted_set):
    return [m for m in all_memes if m['word'] not in posted_set]
