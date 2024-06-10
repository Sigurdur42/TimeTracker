poetry install
pyinstaller ./TimeTracker.spec --noconfirm
mkdir -p ./dist/TimeTracker/
cp ./timetracking/*.ui ./dist/TimeTracker/
cp ./timetracking/*.ico ./dist/TimeTracker/
cp ./timetracking/*.png ./dist/TimeTracker/