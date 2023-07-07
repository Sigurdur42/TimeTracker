from datetime import datetime
from dataclasses import dataclass


@dataclass
class TimeRecord:
    start: datetime
    end: datetime


@dataclass
class ScopeSummary:
    scope: datetime
    working_seconds: int
    overtime_seconds: int
