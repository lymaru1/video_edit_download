import re

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QImage, QPixmap, QIcon, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog

from utils import lym_log
import logging.config

import os, subprocess, time
import cv2


class BodyCut(QWidget):
    video_file: str
    def __init__(self):
        super(BodyCut, self).__init__()
        logging.config.dictConfig(lym_log.LOGGING)
        self.log = logging.getLogger('widget')
        self.base_layout = QVBoxLayout()
        self.file_area = QHBoxLayout()  # 내 파일 찾기
        self.image_area = QHBoxLayout() # 동영상 이미지 영역
        self.file_info_area = QHBoxLayout() # 동영상 정보
        self.time_cut_area = QHBoxLayout()  # 동영상 구간 자르기

        self.init_base_layout()
        self.make_assign_item()

        self.setStyleSheet(
            "QLineEdit{border-radius: 5px;}"
            "QPushButton{border-radius: 5px; border: 2px solid rgb(115, 115, 115);}"
            "QPushButton:hover:!pressed{background-color: rgb(115, 115, 115);}"
            "QPushButton:checked {background-color: rgb(115, 115, 115);}"
            "QToolTip {background-color: rgb(31, 45, 61); color: rgb(255, 255, 255); border: 0px;}"
        )

    def init_base_layout(self):
        self.base_layout.setContentsMargins(10, 20, 10, 20)
        self.base_layout.setSpacing(0)
        self.base_layout.addLayout(self.file_area, 1)
        self.base_layout.addLayout(self.image_area, 7)
        self.base_layout.addLayout(self.file_info_area, 1)
        self.base_layout.addLayout(self.time_cut_area, 1)

        self.setLayout(self.base_layout)

    def make_assign_item(self):
        # file_area 정보
        self.video_file_button = QPushButton()
        self.video_file_button.setIcon(QIcon(':/image/file'))
        self.video_file_button.setIconSize(QSize(40, 40))  # 아이콘 사이즈 설정
        self.video_file_button.setFixedSize(100, 50)
        self.video_file_button.clicked.connect(self.video_file_click)
        self.file_area.addWidget(self.video_file_button)
        self.video_title = QLabel()
        self.video_title.setFixedHeight(50)
        self.video_title.setFont(QFont('Arial', 15))
        self.file_area.addWidget(self.video_title)

        # image_area 정보
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(640, 480)   # 크기 조절
        self.image_area.addWidget(self.thumbnail)

        # file_info_area 정보
        self.video_label = QLabel()
        self.video_label.setFixedHeight(50)
        self.video_label.setFont(QFont('Arial', 15))
        self.file_info_area.addWidget(self.video_label)

        # time_cut_area 정보
        self.start_time = QLineEdit()
        self.start_time.setAlignment(Qt.AlignCenter)    # 가운데 정렬
        self.start_time.setText('00:00:00')
        self.start_time.setFixedHeight(50)
        self.start_time.setFont(QFont('Arial', 15))
        self.time_cut_area.addWidget(self.start_time)
        self.end_time = QLineEdit()
        self.end_time.setAlignment(Qt.AlignCenter)  # 가운데 정렬
        self.end_time.setText('00:00:00')
        self.end_time.setFixedHeight(50)
        self.end_time.setFont(QFont('Arial', 15))
        self.time_cut_area.addWidget(self.end_time)
        self.cut_button = QPushButton()
        self.cut_button.setIcon(QIcon(':/image/start'))
        self.cut_button.setIconSize(QSize(40, 40))  # 아이콘 사이즈 설정
        self.cut_button.setFixedSize(100, 50)
        self.cut_button.clicked.connect(self.cut_click)
        self.time_cut_area.addWidget(self.cut_button)

    def video_file_click(self):
        video_chose_file = QFileDialog.getOpenFileName(self, "Select Video File")
        self.video_file: str = video_chose_file[0]
        self.video_title.setText(os.path.basename(self.video_file))
        try:
            cap = cv2.VideoCapture(self.video_file)
            self.video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
            self.video_label.setText("동영상 시간: " + time.strftime('%H:%M:%S', time.gmtime(self.video_length)))
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    h, w, c = frame.shape   # 높이, 넓이, 채널 추출
                    self.thumbnail.setPixmap(QPixmap.fromImage(QImage(frame.data, w, h, w*c, QImage.Format_BGR888)))    # 이미지 추출 후 섬네일 적용
                    break

        except Exception as e:
            self.video_label.setText("동영상 파일을 불러오는 데 실패하였습니다.")
            self.log.debug(e)

    def cut_click(self):
        start = self.start_time.text()
        end = self.end_time.text()
        try:
            if os.path.isdir("ffmpeg"):
                # ffmpeg 폴더가 있어야함
                ffmpeg_run: str = './ffmpeg/bin/ffmpeg'
            else:
                # ffmpeg 설치되어 있어야함
                ffmpeg_run: str = 'ffmpeg'
            result = subprocess.Popen([ffmpeg_run,
                                       '-i', self.video_file,
                                       '-ss', start,
                                       '-to', end,
                                       '-c', 'copy',
                                       self.video_file.split('.')[0] + 'c.mp4'],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = result.communicate()
            self.log.debug(out.decode('utf-8'))
            self.log.debug(err.decode('utf-8'))
        except Exception as e:
            self.log.debug(e)
