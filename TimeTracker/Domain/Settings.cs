using System;
using System.IO;
using CommunityToolkit.Mvvm.ComponentModel;

namespace TimeTracker.Domain;

[ObservableObject]
public partial record Settings
{
    public string DataFileName { get; set; } = Path.Combine(
        Environment.GetFolderPath(System.Environment.SpecialFolder.UserProfile),
        "TimeTracker",
        "TimeTrackerData.csv");

    [ObservableProperty]
    private TimeSpan _defaultStart = new TimeSpan(8, 0, 0);
    
    [ObservableProperty]
    private TimeSpan _defaultEnd = new TimeSpan(16, 30, 0);
    
    [ObservableProperty]
    private int _defaultPause = 30;
}

public class SettingsRepository
{
    public Settings LoadSettings()
    {
        // TODO: Real load/save logic later on
        return new Settings();
    }
}