using System;
using System.Diagnostics;

namespace TimeTracker.Domain;

[DebuggerDisplay("{Start}->{End} ({Pause})")]
public record TimeRecord
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
