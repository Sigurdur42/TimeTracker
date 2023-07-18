pyinstaller main.py --onefile --noconfirm -n "TimeTracker"
mkdir -p ./dist/src/
cp ./src/*.ui ./dist/src/