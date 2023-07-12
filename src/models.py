from datetime import datetime
from dataclasses import dataclass


@dataclass
class TimeRecord:
    internal_id: int
    start: datetime
    end: datetime

    def scope_as_day(self):
        return self.start.strftime('%d.%m.%Y')

    def get_duration_seconds(self) -> int:
        return (self.end - self.start).seconds

    def get_duration_display(self) -> int:
        diff = self.end - self.start
        return str(diff)


@dataclass
class ScopeSummary:
    scope: datetime
    working_seconds: int
    overtime_seconds: int

    def scope_as_month(self):
        return self.scope.strftime('%m.%Y')

    def scope_as_year(self):
        return self.scope.strftime('%Y')

    def scope_as_day(self):
        return self.scope.strftime('%d.%m.%Y')

    def working_hours(self):
        return self.working_seconds / 60 / 60

    def overtime_hours(self):
        return self.overtime_seconds / 60 / 60
