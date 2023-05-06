using System;
using CommunityToolkit.Mvvm.ComponentModel;

namespace TimeTracker.ViewModels;

[ObservableObject]
public partial class TimeRecordViewModel
{
    [ObservableProperty]
    private DateOnly _day = DateOnly.MinValue;
    
    [ObservableProperty]
    private TimeOnly _start = TimeOnly.MinValue;
    
    [ObservableProperty]
    private TimeOnly _end = TimeOnly.MinValue;

    [ObservableProperty]
    private TimeSpan _pause = TimeSpan.Zero;
    
    [ObservableProperty]
    private TimeSpan _duration = TimeSpan.Zero;
}