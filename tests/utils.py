import json


def get_json_fixture(path: str):
    with open(f'./tests/fixtures/{path}', 'r') as fixture:
        return json.load(fixture)
