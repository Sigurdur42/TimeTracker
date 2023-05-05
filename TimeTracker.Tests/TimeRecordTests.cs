using System;
using System.Globalization;
using NUnit.Framework;
using TimeTracker.Domain;

namespace TimeTracker.Tests;

public class TimeRecordTests
{
    [SetUp]
    public void Setup()
    {
    }

    [TestCase("2014-04-14T08:00:00.00", "16:00:00", "00:00", "8:00", Description = "std 8 hours, no break")]
    [TestCase("2014-04-14T08:00:00.00", "16:00:00", null, "8:00", Description = "std 8 hours, no break")]
    [TestCase("2014-04-14T08:00:00.00", "17:00:00", "00:30", "8:30", Description = "9 hrs with 30min break")]
    [TestCase("2014-04-14T08:00:00.00", null, "00:30", "0:00", Description = "no end")]
    public void VerifyDuration(string start, string? end, string? pause, string expected)
    {
        var culture = new CultureInfo("en-us");
        var target = new TimeRecord()
        {
            Start = DateTime.Parse(start, culture, DateTimeStyles.RoundtripKind),
            End = end != null ? TimeOnly.Parse(end, culture) : null,
            Pause = pause != null ? TimeSpan.Parse(pause, culture) : null
        };

        var result = target.GetDuration();
        Assert.AreEqual(TimeSpan.Parse(expected, culture), result);
    }
}