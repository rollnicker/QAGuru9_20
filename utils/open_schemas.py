import json
from pathlib import Path


def path_name(schema_name):
    return str(Path(__file__).parent.parent.joinpath(f'schemas/{schema_name}'))


def load_schema(path=""):
    with open(path_name(path)) as file:
        return json.loads(file.read())
