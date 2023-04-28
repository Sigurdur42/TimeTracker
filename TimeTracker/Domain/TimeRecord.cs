using System;

namespace TimeTracker.Domain;

public class TimeRecord
{
    public DateOnly Day { get; set; }
    public TimeOnly Start { get; set; }
    public TimeOnly? End { get; set; }
    public TimeSpan? Pause { get; set; }
    
}
