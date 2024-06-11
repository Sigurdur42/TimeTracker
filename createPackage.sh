poetry install
if [ $? -eq 0 ]
then
  echo "successfully installed poetry dependencies"
else
  echo "poetry install failed" >&2
  exit $?
fi

poetry build
if [ $? -eq 0 ]
then
  echo "successfully called poetry build"
else
  echo "poetry build failed" >&2
  exit $?
fi

pyinstaller ./TimeTracker.spec --noconfirm
if [ $? -eq 0 ]
then
  echo "successfully build using pyinstaller"
else
  echo "pyinstaller build failed" >&2
  exit $?
fi