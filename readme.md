- [ ] Fill this with content
- define csv content
- convert excel data to csv
- load csv content from ~/TimeTracker/TimeTrackerData.csv

# todo
- add logging
- design UI
  - react on resize
  - error handling

# References
- https://betterprogramming.pub/get-started-with-pyqt-and-qt-designer-63955a129cf7
- https://dev.to/flet/build-and-deploy-a-web-app-in-python-without-knowledge-of-html-css-javascript-30hl

- https://pypi.org/project/pip-autoremove/

# Installation
## Restore python environment
In the cloned git folder:
``` 
python -m venv /path/to/new/virtual/environment
pip install -r requirements.txt
``` 

## Create/Update python environment
```
pip freeze > requirements.txt
```

## Create Distribution Package
### Linux
This script will create the executable single file and copy the required UI files.
```
./createPackage.sh
```


### Windows
This script will create the executable single file and copy the required UI files.
```
./createPackage.bat
```