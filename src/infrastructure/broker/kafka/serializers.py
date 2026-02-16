import json


def serialize(value: dict) -> bytes:
    return json.dumps(value).encode("utf-8")


def deserialize(value: bytes) -> dict:
    return json.loads(value.decode("utf-8"))
