pip install -r requirements.txt
pyinstaller main.py --onefile --noconfirm -n "TimeTracker"
mkdir -p ./dist/src/
cp ./src/*.ui ./dist/src/
cp ./src/*.ico ./dist/src/
cp ./src/*.png ./dist/src/