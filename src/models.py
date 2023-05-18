from datetime import date, time
from dataclasses import dataclass

@dataclass
class TimeRecord:    
    day : date
    start: time
    end: time
    