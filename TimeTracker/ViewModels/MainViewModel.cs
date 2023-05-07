using System;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Net;
using System.Windows.Input;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using TimeTracker.Domain;

namespace TimeTracker.ViewModels;

[ObservableObject]
public partial class MainViewModel
{
    private readonly Settings _settings;

    public MainViewModel()
    {
        _newItemCommand = new RelayCommand(AddNewRecord);
        var version = GetType()?.Assembly?.GetName()?.Version?.ToString() ?? "<unknown>";
        _title = $"Time Tracker by Papsi - {version}";

        var settingsRepository = new SettingsRepository();
        _settings = settingsRepository.LoadSettings();

        LoadDataFile();
    }

    [ObservableProperty] private string _title;

    [ObservableProperty] private ObservableCollection<TimeRecordViewModel> _timeRecords = new();
    [ObservableProperty] private ICommand _newItemCommand;
    [ObservableProperty] private TimeRecordViewModel? _selectedRecord;

    private void AddNewRecord()
    {
        var newItem = new TimeRecordViewModel()
        {
            Day = new DateTimeOffset(DateTime.Now),
            Start = _settings.DefaultStart,
            End = _settings.DefaultEnd,
            PauseInMinutes = _settings.DefaultPause,
        };

        _timeRecords.Add(newItem);
        SelectedRecord = newItem;
    }

    private void LoadDataFile()
    {
        try
        {
            var deserialize = new TimeRecordRepository();
            var rawData = deserialize.Deserialize(new FileInfo(_settings.DataFileName));

            var viewModels = rawData.Select(_ => new TimeRecordViewModel()
            {
                Day = new DateTimeOffset(_.Start),
                Start = new TimeSpan(_.Start.Hour, _.Start.Minute, _.Start.Second),
                End = _.End.HasValue ?  new TimeSpan(_.End.Value.Hour, _.End.Value.Minute, _.End.Value.Second) : TimeSpan.Zero,
                PauseInMinutes = (int)(_.Pause?.TotalMinutes ?? 0),
                Duration = _.GetDuration()
            }).ToArray();

            TimeRecords = new ObservableCollection<TimeRecordViewModel>(viewModels);
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
            // TODO:Handle this correctly
        }
    }
}