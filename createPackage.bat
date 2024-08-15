echo off
poetry install
if %ERRORLEVEL% == 0 (
	echo "successfully installed poetry dependencies"
) else (
  echo "poetry install failed" 
  cmd /c exit %errorlevel%
  goto END
)

poetry build
if %ERRORLEVEL% == 0 (
	echo "successfully called poetry build"
) else (
  echo "poetry build failed" 
  cmd /c exit %errorlevel%
  goto END
)

pyinstaller ./TimeTracker.spec --noconfirm
if %ERRORLEVEL% EQU 0 (
	echo "successfully build using pyinstaller"
) else (
  echo "pyinstaller build failed" 
  cmd /c exit %errorlevel%
  goto END
)

cmd /c exit 0

:END