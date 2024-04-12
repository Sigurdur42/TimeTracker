pip install -r requirements.txt
pyinstaller ./TimeTracker.spec --noconfirm
mkdir -p ./dist/src/
cp ./src/*.ui ./dist/src/
cp ./src/*.ico ./dist/src/
cp ./src/*.png ./dist/src/