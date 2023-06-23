from datetime import datetime
from dataclasses import dataclass


@dataclass
class TimeRecord:
    start: datetime
    end: datetime


@dataclass
class SingleDaySummary:
    day: datetime
    working_seconds: int


@dataclass
class SingleMonthSummary:
    month: datetime
    working_seconds: int


@dataclass
class SingleYearSummary:
    month: datetime
    working_seconds: int
