from enum import StrEnum, auto
from pydantic import BaseModel, Field, computed_field
from datetime import datetime

class Priority(StrEnum):
    """
    Task priority classification based on the Eisenhower Matrix.

    Each value represents a combination of urgency and importance:
    - DO = urgent and important - requires immediate action.
    - SCHEDULE = important but not urgent - plan and execute later.
    - DELEGATE = urgent but not important - assign to someone else.
    - ELIMINATE = neither urgent nor important - delete or ignore
    - UNKNOWN = insufficient data to determine priority
    """
    DO = auto()
    SCHEDULE = auto()
    DELEGATE = auto()
    ELIMINATE = auto()
    UNKNOWN = auto()

class Urgency(StrEnum):
    """
    Urgency classification used as an input signal for priority determination.
    Indicates time sensitivity of a task, independent of its importance.
    """
    UNKNOWN = auto()
    URGENT = auto()
    NOT_URGENT = auto()

class Importance(StrEnum):
    """
    Importance classification used as an input signal for priority determination.
    Indicates the long-term value or impact of a task, independent of urgency.
    """
    UNKNOWN = auto() 
    IMPORTANT = auto()
    NOT_IMPORTANT = auto()

class Task(BaseModel):
    """
    Structured representation of a single extracted task.
    Combines raw extracted hints with normalized classification signals 
    (urgency, importance) and derives a priority quadrant.
    """

    title: str
    
    description: str | None = Field (
            default = None,
            description = "Optional explanation or context of task."
    )
    
    assignee_hint: str | None = Field(
            default = None,
            description = "Free-text hint indicating who is responsible for the task, if identifiable"
    )
    
    deadline_hint: str | None = Field (
            default = None,
            description = "Free-text hint describing when the task is due."
    )
    
    urgency: Urgency = Field(
            default = Urgency.UNKNOWN,
            description = "Estimated urgency level derived from the source text."
    )
    
    importance: Importance = Field (
            default = Importance.UNKNOWN,
            description = "Estimated importance level derived from the source text."
    )
    
    confidence: float = Field(
            ge=0.0, 
            le=1.0, 
            default = 0.0,
            description = "Model confidence score (0.0-1.0) for the extracted task and its classification"
    )
    
    @computed_field (description = "Derived priority classification based on urgency and importance.")
    @property
    def quadrant(self) -> Priority:
        """Maps urgency and importance to a Priority (Eisenhower quadrant)."""
        if self.urgency == Urgency.URGENT and self.importance == Importance.IMPORTANT:
            return Priority.DO
        elif self.urgency == Urgency.URGENT and self.importance == Importance.NOT_IMPORTANT:
            return Priority.DELEGATE
        elif self.urgency == Urgency.NOT_URGENT and self.importance == Importance.IMPORTANT:
            return Priority.SCHEDULE
        elif self.urgency == Urgency.NOT_URGENT and self.importance == Importance.NOT_IMPORTANT:
            return Priority.ELIMINATE
        else:
            return Priority.UNKNOWN

class ExtractionResult(BaseModel):
    """
    Container for the output of a task extraction process.
    Includes extracted task along with metadata about the source input and the model execution context.
    """
    
    tasks: list[Task] = Field (
            description = "List of structured tasks extracted from the input text."
    )
    
    source_text_preview: str = Field (
            description = "Truncated preview of the original input text used for extraction (200 character limit)."
    )
    
    extracted_at: datetime = Field (
            description = "Timestamp indicating when the extraction was performed."
    )
    
    model_used: str = Field (
            description = "Identifier of the model used to perform the extraction."
    )
    
    token_usage: dict | None = Field (
            default = None,
            description = "Optional token usage metadata."
    )
