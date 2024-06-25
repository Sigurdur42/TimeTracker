from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class TimeRecord:
    internal_id: int
    start: datetime
    end: datetime
    all_overtime: bool
    comment: Optional[str]

    def scope_as_day(self):
        return self.start.strftime("%d.%m.%Y")

    def get_duration_seconds(self) -> int:
        return (self.end - self.start).seconds

    def get_duration_display(self) -> int:
        diff = self.end - self.start
        return str(diff)

    def get_main_comment(self) -> str:
        if self.comment is None:
            return None

        parts = self.comment.split(':')
        return parts[0].strip()


@dataclass
class ScopeSummary:
    scope: datetime
    working_seconds: int
    overtime_seconds: int
    comment: str = None

    def scope_as_month(self):
        return self.scope.strftime("%m.%Y")

    def scope_as_year(self):
        return self.scope.strftime("%Y")

    def scope_as_day(self):
        return self.scope.strftime("%d.%m.%Y")

    def working_hours(self):
        return self.working_seconds / 60 / 60

    def overtime_hours(self):
        return self.overtime_seconds / 60 / 60


@dataclass
class TimesheetRecord:
    scope: datetime
    start: str
    end: str
    pause: str
    travel_start: str
    travel_end: str

    def scope_as_day(self):
        return self.scope.strftime("%d.%m.%Y")


@dataclass
class HumanReadable:
    @staticmethod
    def seconds_to_human_readable(seconds: int) -> str:
        hours = abs(int(seconds / 60 / 60))
        minutes = int(seconds / 60 % 60)
        if seconds < 0 and minutes != 0:
            minutes = 60 - int(seconds / 60 % 60)

        sign = "-" if seconds < 0 else ""
        return f"{sign}{hours:02d}:{minutes:02d}"

    @staticmethod
    def seconds_to_decimal_display(seconds: int) -> str:
        hours = seconds / 60 / 60
        return f"{hours:.02f}"
