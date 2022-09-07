import json
import os


def get_json_fixture(path: str):
    with open(f'{os.getcwd()}/tests/fixtures/{path}', 'r') as fixture:
        return json.load(fixture)
