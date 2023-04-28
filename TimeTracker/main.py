from datetime import datetime, timedelta

from domainModels import TimeRecord

record = TimeRecord(
    start=datetime(2023, 4, 23, 8, 12),
    end=datetime(2023, 4, 23, 18, 12),
    pause=timedelta(minutes=30))
record.update_duration()
print(record)
print(record.duration.total_seconds() / 60 / 60)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           