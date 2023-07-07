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
