import json
from extractbot.models import Task
from extractbot.extractor import EXTRACTION_TOOL

def test_schema_is_json_serializable():
    json.dumps(EXTRACTION_TOOL)

def test_schema_fields_match_model_fields():
    schema_fields = set(EXTRACTION_TOOL["parameters"]["properties"]["tasks"]["items"]["properties"].keys())
    model_fields = set(Task.model_fields.keys())

    assert schema_fields == model_fields
