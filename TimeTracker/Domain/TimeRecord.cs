using System;

namespace TimeTracker.Domain;

public class TimeRecord
{
    public DateTime Start { get; set; }
    public TimeOnly? End { get; set; }
    public TimeSpan? Pause { get; set; }

    public TimeSpan GetDuration()
    {
        if (!End.HasValue)
        {
            return new TimeSpan();
        }

        var result = End.Value - TimeOnly.FromDateTime(Start);
        if (Pause.HasValue)
        {
            result -= Pause.Value;
        }

        return result;
    }
}
