from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox

from utils import lym_log
import logging.config


class MenuContents(QWidget):
    def __init__(self, parent):
        super(MenuContents, self).__init__(parent)
        self.parent = parent  # 부모 저장
        logging.config.dictConfig(lym_log.LOGGING)
        self.log = logging.getLogger('widget')

        self.base_layout = QVBoxLayout()
        self.contents_area = QVBoxLayout()    # 컨텐츠 영역
        self.info_area = QVBoxLayout()    # 정보 영역

        self.init_base_layout()
        self.make_assign_item()

        self.setStyleSheet(
            "QPushButton{border-radius: 5px;}"
            "QPushButton:hover:!pressed{background-color: rgb(115, 115, 115);}"
            "QPushButton:checked {background-color: rgb(115, 115, 115);}"
            "QToolTip {background-color: rgb(31, 45, 61); color: rgb(255, 255, 255); border: 0px;}"
        )
        self.setLayout(self.base_layout)
        background = QPalette()  # 창에 색상 적용 가능하게 팔레트 호출
        background.setColor(self.backgroundRole(), QColor(230, 230, 230))  # 창 배경에 적용할 색을 저장
        self.setPalette(background)  # 색상 적용
        self.setAutoFillBackground(True)

    def init_base_layout(self):
        self.base_layout.setContentsMargins(10, 10, 10, 10)
        self.base_layout.setSpacing(10)
        self.base_layout.addLayout(self.contents_area, 9)
        self.base_layout.addLayout(self.info_area, 1)

    def make_assign_item(self):
        # contents_area 영역
        self.contents_area.setAlignment(Qt.AlignTop)  # 상단 정렬
        self.video_download_button = QPushButton()
        self.video_download_button.setObjectName('video_download_button')
        self.video_download_button.setIcon(QIcon(':/image/download.png'))    # 이미지 설정
        self.video_download_button.setIconSize(QSize(40, 40))  # 아이콘 사이즈 설정
        self.video_download_button.setMinimumSize(50, 50)  # 미니멈 사이즈 설정
        self.video_download_button.clicked.connect(lambda: self.function_change_object('video_download'))
        self.video_download_button.setToolTip(f"video_download_button")
        self.video_download_button.setCheckable(True)
        self.video_download_button.setChecked(True)
        self.contents_area.addWidget(self.video_download_button)

        self.video_cut_button = QPushButton()
        self.video_cut_button.setObjectName('video_cut_button')
        self.video_cut_button.setIcon(QIcon(':/image/cut.png'))  # 이미지 설정
        self.video_cut_button.setIconSize(QSize(40, 40))  # 아이콘 사이즈 설정
        self.video_cut_button.setMinimumSize(50, 50)  # 미니멈 사이즈 설정
        self.video_cut_button.clicked.connect(lambda: self.function_change_object('video_cut'))
        self.video_cut_button.setToolTip(f"video_cut_button")
        self.video_cut_button.setCheckable(True)
        self.contents_area.addWidget(self.video_cut_button)

        # info_area 영역
        self.info_area.setAlignment(Qt.AlignBottom)  # 하단 정렬
        self.info_button = QPushButton()
        self.info_button.setObjectName('info_button')
        self.info_button.setIcon(QIcon(':/image/info.png'))  # 이미지 설정
        self.info_button.setIconSize(QSize(40, 40))  # 아이콘 사이즈 설정
        self.info_button.setMinimumSize(50, 50)  # 미니멈 사이즈 설정
        self.info_button.clicked.connect(self.info_click)
        self.info_button.setToolTip(f"info_button")
        self.info_area.addWidget(self.info_button)

    def function_change_object(self, function_name: str):
        """
        기능별 클래스를 지정 해주며 상단 해더 부분에 목록을 변경해준다.
        :param function_name: 기능 별 class 객체
        """
        self.button_checked_item(function_name+"_button")
        # 위젯 오브젝트 이름으로 설정
        for widget in self.parent.body_contents_get_widget_list():
            if isinstance(widget, QWidget):
                if widget.objectName() == function_name:
                    self.parent.body_contents_change(widget)

    def button_checked_item(self, button_name: str):
        """
        선택 되어 있는 버튼을 번경해준다.
        :param button_name: 버튼별 이름
        """
        for i in range(self.base_layout.count()):
            item: QPushButton = self.contents_area.itemAt(i).widget()
            if isinstance(item, QPushButton):
                if button_name == item.objectName():
                    item.setChecked(True)
                else:
                    item.setChecked(False)

    def info_click(self):
        msg = QMessageBox()
        msg.setWindowTitle("사용 설명서")
        msg.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowCloseButtonHint)
        msg.setText(f"사용설명서")
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        # with oepn('document.txt','r') as file:
        #     msg.setDetailedText(file.readlines())
        msg.setDetailedText("""
## 사용 설명서

## 왼쪽 이모티콘 메뉴
1. 유튜브 다운로드
2. 동영상 자르기
3. 사용 설명서

## 유튜브 다운로드
1. 상단 왼쪽 유트브 링크를 입력한다.
2. 상단 오른쪽 버튼을 눌러 검색을 한다.
3. 중간에 썸네일이 나올 경우 하단 왼쪽에 제목이 맞는지 확인 한다.
4. 하단 오른쪽 버튼을 눌러 다운로드를 진행한다.
3-1. 중간에 이미지가 않나오고 하단 왼쪽에 '동영상 주소 검색에 실패하였습니다.'가 나올경우 1번에 링크를 다시 작성한다.

## 동영상 자르기
1. 상단 왼쪽 버튼을 눌러 자를 동영상을 찾는다.
2. 상단 오른쪽 동영상 이름 및 중간에 동영상 이미지 및 동영상의 길이 정보를 확인한다.
3. 하단 왼쪽에 시작 시간 및 끝나는 시간을 작성한다.
3-1) 양식은 '시간 : 분 : 초' 로 입력하는데 중간에 `:`가 있어야 하며 공백이 없어야한다.
4. 하단 오른쪽에 실행 버튼을 누르면 동영상이 잘라진다. 위치는 편집하는 동영상 위치에 생성이된다. [이름에 `cut`이 마지막에 추가되어 생성]


## license
- pyside6
- opencv-python
- pytube

## icon
- flaticon
            """)
        msg.setStyleSheet("""
                        QMessageBox {background-color: #EEEEEE; border: 1px solid #202020}
                        QMessageBox QLabel {min-width: 650px; color: #202020;}
                        QScrollArea {border: none;}
                        QScrollBar {border-radius: 5px;}
                        QScrollBar:horizontal {height: 5px;}
                        QScrollBar:vertical {width: 5px;}
                        QScrollBar::handle {background: rgb(115, 115, 115); border-radius: 2px;}
                        QScrollBar::handle:horizontal {height: 5px; min-width: 5px;}
                        QScrollBar::handle:vertical {width: 5px; min-height: 5px;}
                        QScrollBar::add-line, QScrollBar::sub-line {border: none; background: none;}
                        QPushButton {min-width: 100px; background-color: #EEEEEE; color: #202020;}
                        QTextEdit {background-color: #EEEEEE; color: #202020; min-height: 200px;}
                    """)
        msg.exec()
