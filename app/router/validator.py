import json
from pydantic import BaseModel, ValidationError

def validate_and_parse(schema: type[BaseModel], raw: str):
    data = json.loads(raw)
    return schema.model_validate(data)
