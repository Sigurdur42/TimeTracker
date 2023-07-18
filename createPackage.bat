pyinstaller main.py -n "TimeTracker" --noconfirm --add-binary "src/MainWindow.ui;src/." --add-binary "src/EditRecord.ui;src/."
If exist ".\dist\src" ( 
    Echo "dist\src already exists"
) Else ( 
    Echo "creating ui folder"
    mkdir ".\dist\src"
)
copy .\src\*.ui .\dist\src