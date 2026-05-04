from enum import StrEnum, auto
from pydantic import BaseModel, Field
from datetime import datetime

class Priority(StrEnum):
    DO = auto()
    SCHEDULE = auto()
    DELEGATE = auto()
    ELIMINATE = auto()

class Urgency(StrEnum):
    UNKNOWN = auto()
    URGENT = auto()
    NOT_URGENT = auto()

class Importance(StrEnum):
    UNKNOWN = auto() 
    IMPORTANT = auto()
    NOT_IMPORTANT = auto()

class Task(BaseModel):
    title: str
    description: str | None = None
    assignee_hint: str | None = None
    deadline_hint: str | None = None
    urgency: Urgency = Urgency.UNKNOWN
    importance: Importance = Importance.UNKNOWN
    confidence: float = Field(ge=0.0, le=1.0, default = 0.0)

class ExtractionResult(BaseModel):
    tasks: list[Task]
    source_text_preview: str
    extracted_at: datetime
    model_used: str
    token_usage: dict | None = None
