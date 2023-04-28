from datetime import date, time
from domain import TimeRecord

record = TimeRecord(date(2023, 4,23), time(8, 12), time(18, 12), 30)
record.updateDuration()
print(record)