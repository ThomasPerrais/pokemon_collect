import json


def read_objects_from_array_json(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_objects_from_json(file_path: str) -> list[dict]:
    objects = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            obj = json.loads(line)
            objects.append(obj)
        return objects
