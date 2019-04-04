FROM python:3.6-windowsservercore-1809



ADD requirements-tests.txt requirements.txt /
RUN ( C:\Python\python.exe -m pip install --upgrade-strategy eager -U -r requirements-tests.txt ) -and \
    ( C:\Python\python.exe -m pip install --upgrade-strategy eager -U -r requirements.txt ) -and \
    ( Remove-Item –path %LOCALAPPDATA%\pip\Cache -recurse -ErrorAction Ignore )
