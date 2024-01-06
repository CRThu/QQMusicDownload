import json


def store_json(filename, obj):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
