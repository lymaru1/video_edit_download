# Video Edit Download

***
## 환경
- windows10
- python 3.9.13
- ffmpeg

***
## python
- numpy==1.23.4
- opencv-python==4.6.0.66
- PySide6==6.4.0.1
- PySide6-Addons==6.4.0.1
- PySide6-Essentials==6.4.0.1
- pytube==12.1.0
- shiboken6==6.4.0.1
- wincertstore==0.2

***
## 기본 세팅
pip install pyside6 opencv-python

ffmpeg 공식 홈페이지에서 build 된 essentials 파일을 받아 ffmpeg 폴더로 압축을 풀어준다.

***
## 파일 exe
pyinstaller --clean -w --icon=logo.ico -F -n 위클리 main.py

***
