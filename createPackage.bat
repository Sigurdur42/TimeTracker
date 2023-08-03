pip install -r requirements.txt
pyinstaller .\TimeTracker.spec --noconfirm
If exist ".\dist\src" ( 
    Echo "dist\src already exists"
) Else ( 
    Echo "creating ui folder"
    mkdir ".\dist\src"
)
copy .\src\*.ui .\dist\TimeTracker\src
copy .\src\*.ico .\dist\TimeTracker\src
copy .\src\*.png .\dist\TimeTracker\src