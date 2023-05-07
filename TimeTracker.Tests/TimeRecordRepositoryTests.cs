using System;
using System.Collections;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using NUnit.Framework;
using TimeTracker.Domain;

namespace TimeTracker.Tests;

[TestFixture]
public class TimeRecordRepositoryTests
{
    [Test]
    public void SerializeAndDeserializeTest()
    {
        var tempFile = new FileInfo(Path.GetTempFileName());
        try
        {
            var target = new TimeRecordRepository();
            var dataToWrite = GenerateTestData();
            target.Serialize(dataToWrite, tempFile);

            var readData = target.Deserialize(tempFile);
            CollectionAssert.AreEqual(dataToWrite, readData);
        }
        finally
        {
            if (tempFile.Exists)
            {
                tempFile.Delete();
            }
        }
    }

    private TimeRecord[] GenerateTestData()
    {
        var random = new Random();
        const int firstHour = 7;
        var firstDay = new DateTime(2023, 01, 02, firstHour, 0, 0);
        var result = new List<TimeRecord>();
        for (var index = 0; index < 100; ++index)
        {
            result.Add(new TimeRecord()
            {
                Start = firstDay.AddDays(index),
                End = new TimeOnly(firstHour + random.Next(10), 0, 0),
                Pause = new TimeSpan(0, random.Next(59), 0)
            });
        }

        // add some data for null handling
        result.Add(new TimeRecord()
        {
            Start = firstDay.AddDays(200),
            End = null,
            Pause = null,
        });

        result.Add(new TimeRecord()
        {
            Start = firstDay.AddDays(201),
            End = new TimeOnly(firstHour + random.Next(10), 0, 0),
            Pause = null,
        });

        result.Add(new TimeRecord()
        {
            Start = firstDay.AddDays(202),
            End = null,
            Pause = new TimeSpan(0, random.Next(59), 0),
        });

        return result.ToArray();
    }
}