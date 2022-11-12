from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QImage, QPixmap, QIcon, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit

from utils import lym_log
import logging.config

import pytube
import os, urllib.request


class BodyDownload(QWidget):
    youtube: pytube.YouTube

    def __init__(self):
        super(BodyDownload, self).__init__()
        logging.config.dictConfig(lym_log.LOGGING)
        self.log = logging.getLogger('widget')
        self.base_layout = QVBoxLayout()
        self.search_area = QHBoxLayout()
        self.image_area = QHBoxLayout()
        self.download_area = QHBoxLayout()

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
        self.base_layout.addLayout(self.search_area, 1)
        self.base_layout.addLayout(self.image_area, 8)
        self.base_layout.addLayout(self.download_area, 1)

        self.setLayout(self.base_layout)

    def make_assign_item(self):
        # search_area 정보
        self.search_url = QLineEdit()   # 비디오 검색
        self.search_url.setPlaceholderText("주소를 입력해 주세요.")
        self.search_url.setFixedHeight(50)  #
        self.search_url.setFont(QFont('Arial', 15))
        self.search_url.returnPressed.connect(self.search_button_click)
        self.search_area.addWidget(self.search_url)
        self.search_button = QPushButton()
        self.search_button.setIcon(QIcon(':/image/search.png'))    # 이미지 설정
        self.search_button.setIconSize(QSize(40, 40))  # 아이콘 사이즈 설정
        self.search_button.setFixedSize(150, 50)
        self.search_button.clicked.connect(self.search_button_click)
        self.search_area.addWidget(self.search_button)

        # image_area 정보
        self.thumbnail = QLabel()
        self.image_area.setAlignment(Qt.AlignCenter)
        self.image_area.addWidget(self.thumbnail)

        # download_area 정보
        self.video_title = QLabel() # 비디오 이름
        self.video_title.setFixedHeight(50)
        self.video_title.setFont(QFont('Arial', 15))
        self.download_area.addWidget(self.video_title)
        self.download_button = QPushButton()
        self.download_button.clicked.connect(self.download_button_click)
        self.download_button.setIcon(QIcon(':/image/video_download.png'))  # 이미지 설정
        self.download_button.setIconSize(QSize(40, 40))  # 아이콘 사이즈 설정
        self.download_button.setFixedSize(150, 50)
        self.download_button.hide()
        self.download_area.addWidget(self.download_button)

    def search_button_click(self):
        url: str = self.search_url.text()
        try:
            self.youtube = pytube.YouTube(url)
            image_from_web = urllib.request.urlopen(self.youtube.thumbnail_url).read()
            self.thumbnail.setPixmap(QPixmap.fromImage(QImage.fromData(image_from_web)))
            self.video_title.setText(self.youtube.title)
            self.download_button.show()
        except Exception as e:
            self.video_title.setText("동영상 주소 검색에 실패하였습니다.")
            self.log.debug(e)

    def download_button_click(self):
        if os.path.isdir('download') is False:
            os.mkdir('download')
        self.youtube.streams.get_highest_resolution().download('download')
