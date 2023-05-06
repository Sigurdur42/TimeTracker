using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using CsvHelper;
using CsvHelper.Configuration;

namespace TimeTracker.Domain;

public class TimeRecordRepository
{
    private readonly  CsvConfiguration _configuration;
    public TimeRecordRepository()
    {
        _configuration = new CsvConfiguration(CultureInfo.InvariantCulture)
        {
            NewLine = Environment.NewLine,
        };
    }
    
    public void Serialize(IEnumerable<TimeRecord> timeRecords, FileInfo fileName)
    {
        using var writer = new StreamWriter(fileName.FullName);
        using var csv = new CsvWriter(writer, _configuration);
        csv.WriteRecords(timeRecords);
    }

    public IEnumerable<TimeRecord> Deserialize(FileInfo file)
    {
        using var reader = new StreamReader(file.FullName);
        using var csv = new CsvReader(reader, _configuration);
        return csv.GetRecords<TimeRecord>().ToArray();
    }
}