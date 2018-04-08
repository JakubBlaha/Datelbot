pyinstaller^
 --onefile^
 --windowed^
 --add-binary img/icon.ico;img^
 --icon img/icon.ico^
 --version-file version.py^
 --name datelbot.exe^
 source.py