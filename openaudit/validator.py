"""
OpenAudit Validator
===================
Validates audit events against the OpenAudit JSON Schema.
"""

import json
from pathlib import Path
from jsonschema import validate, ValidationError

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "open_audit_schema.json"


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def validate_event(event):
    """Validate a single event against the schema. Returns (ok: bool, error: str|None)."""
    schema = load_schema()
    try:
        validate(instance=event, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)


def validate_file(filepath):
    """Validate a JSON or JSONL file. Returns (ok: bool, error: str|None)."""
    path = Path(filepath)
    with open(path) as f:
        if path.suffix == ".jsonl":
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                event = json.loads(line)
                ok, err = validate_event(event)
                if not ok:
                    return False, f"Line {i+1}: {err}"
        else:
            data = json.load(f)
            if isinstance(data, list):
                for i, event in enumerate(data):
                    ok, err = validate_event(event)
                    if not ok:
                        return False, f"Index {i}: {err}"
            else:
                return validate_event(data)
    return True, None
