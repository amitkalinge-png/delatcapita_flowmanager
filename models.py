# models.py
from typing import Any, Dict, Optional, List
from pydantic import BaseModel


class TaskResult(BaseModel):
    status: str  # success/failure
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


class TaskSpec(BaseModel):
    name: str
    description: Optional[str] = None


class ConditionSpec(BaseModel):
    name: str
    source_task: str
    outcome: str
    target_task_success: str
    target_task_failure: str
    description: Optional[str] = None


class FlowSpec(BaseModel):
    id: str
    name: str
    start_task: str
    tasks: List[TaskSpec]
    conditions: List[ConditionSpec]


class FlowFile(BaseModel):
    flow: FlowSpec
