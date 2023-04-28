from dataclasses import dataclass, field
from datetime import datetime
from datetime import timedelta


@dataclass
class TimeRecord:
    start: datetime = field(default=0)
    end: datetime = field(default=0)
    pause: timedelta = field(default=0)
    duration: timedelta = field(default=0)

    def update_duration(self):
        self.duration = timedelta(0)
        if self.end > self.start:
            self.duration = self.end - self.start
            
            if self.pause.total_seconds() > 0:
                self.duration = self.duration - self.pause
