using System;
using CommunityToolkit.Mvvm.ComponentModel;

namespace TimeTracker.ViewModels;

[ObservableObject]
public partial class TimeRecordViewModel
{
    [ObservableProperty]
    private DateTimeOffset _day = DateTimeOffset.MinValue;
    
    [ObservableProperty]
    private TimeSpan _start = TimeSpan.MinValue;
    
    [ObservableProperty]
    private TimeSpan _end = TimeSpan.Zero;

    [ObservableProperty]
    private int _pauseInMinutes = 0;
    
    [ObservableProperty]
    private TimeSpan _duration = TimeSpan.Zero;
}