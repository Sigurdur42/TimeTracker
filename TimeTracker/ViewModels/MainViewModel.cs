using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;

namespace TimeTracker.ViewModels;

[ObservableObject]
public partial class MainViewModel
{
    public MainViewModel()
    {
        var version = GetType()?.Assembly?.GetName()?.Version?.ToString() ?? "<unknown>";
        _title = $"Time Tracker by Papsi - {version}";
    }
    
    [ObservableProperty] private string _title;

    [ObservableProperty]
    private ObservableCollection<TimeRecordViewModel> _timeRecords = new();
}