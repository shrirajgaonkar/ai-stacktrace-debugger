from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any

class RootCauseItem(BaseModel):
    title: str
    confidence: float
    evidence: List[str]
    reasoning: str

class RootCausesSchema(BaseModel):
    runtime: str
    exception_type: str
    root_causes: List[RootCauseItem]

class CodeSnippet(BaseModel):
    language: str
    code: str

class FixStepItem(BaseModel):
    title: str
    steps: List[str]
    code_snippets: List[CodeSnippet]
    risk: str
    evidence: List[str]

class FixStepsSchema(BaseModel):
    fixes: List[FixStepItem]

def validate_root_causes(data: dict) -> bool:
    try:
        RootCausesSchema(**data)
        return True
    except ValidationError:
        return False

def validate_fix_steps(data: dict) -> bool:
    try:
        FixStepsSchema(**data)
        return True
    except ValidationError:
        return False
