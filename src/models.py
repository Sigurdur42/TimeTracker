from datetime import datetime
from dataclasses import dataclass


@dataclass
class TimeRecord:
    start: datetime
    end: datetime


@dataclass
class SingleDaySummary:
    scope: datetime
    working_seconds: int
    overtime_seconds: int


@dataclass
class SingleMonthSummary:
    scope: datetime
    working_seconds: int
    overtime_seconds: int


@dataclass
class SingleYearSummary:
    scope: datetime
    working_seconds: int
    overtime_seconds: int
