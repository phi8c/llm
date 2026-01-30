from pydantic import BaseModel
from typing import List

class AdminOutput(BaseModel):
    summary: str
    risks: List[str]
    next_steps: List[str]

class HrOutput(BaseModel):
    summary: str
    policy_reference: str

class StaffOutput(BaseModel):
    summary: str
    todo: List[str]


SCHEMA_BY_ROLE = {
    "admin": AdminOutput,
    "hr": HrOutput,
    "staff": StaffOutput,
}
