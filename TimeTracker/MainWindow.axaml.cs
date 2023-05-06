using Avalonia.Controls;

namespace TimeTracker;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        this.DataContext = new ViewModels.MainViewModel();
    }
}