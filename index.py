from PySide6.QtGui import QIcon, QColor, QPalette
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QWidget

from utils import lym_log
import logging.config

from utils import menu_contents, body_contents


import image_rcc   # pyside 이미지 경로 찾아가는 모듈

class MainUI(QMainWindow):
    def __init__(self, width: float, height: float):
        super(MainUI, self).__init__()
        logging.config.dictConfig(lym_log.LOGGING)
        self.log = logging.getLogger('widget')
        self.screen_width: int = int(width * 0.5)    # 창 크기 설정
        self.screen_height: int = int(height * 0.5)   # 창 크기 설정
        self.init_window()  # 윈도우 설정

        self.base_layout = QHBoxLayout()    # 전체 레이아웃
        self.base_menu_contents_widget = menu_contents.MenuContents(self)   # 메뉴 (다운로드, 자르기)
        self.base_body_contents_widget = body_contents.BodyContents(self)   # 컨텐츠 (다운로드, 자르기)

        self.init_base_layout()

        widget = QWidget()
        widget.setLayout(self.base_layout)
        self.setCentralWidget(widget)

    def init_window(self):
        """
        윈도우 창 세팅
        """
        self.setWindowTitle('wicly')   # 윈도우 창 이름 설정
        self.setWindowIcon(QIcon(":/image/logo.png"))   # 프로그램 창의 아이콘 설정
        self.resize(self.screen_width, self.screen_height)  # 프로그램 창 사이즈 설정

        background = QPalette()   # 창에 색상 적용 가능하게 팔레트 호출
        background.setColor(self.backgroundRole(), QColor(255, 255, 255))    # 창 배경에 적용할 색을 저장
        self.setPalette(background) # 색상 적용

    def init_base_layout(self):
        """
        base layout 위젯 및 레이아웃 할당
        """
        self.setLayout(self.base_layout)
        self.base_layout.addWidget(self.base_menu_contents_widget, 1)
        self.base_layout.addWidget(self.base_body_contents_widget, 9)

        self.base_layout.setContentsMargins(0, 0, 0, 0) # 메인 레이아웃 margin은 0으로 설정
        self.base_layout.setSpacing(0)  # 레이아웃 간의 간격은 0으로 설정

    def body_contents_change(self, widget):
        """
        base_body_contents_widget에 선택한 위젯으로 변경
        :param: 컨텐츠 위젯
        """
        self.base_body_contents_widget.contents_change(widget)

    def body_contents_get_widget_list(self) -> list:
        """
        base_body_contents_widget에 위젯을 요청
        :return: 컨텐츠 위젯 리스트
        """
        return self.base_body_contents_widget.contents_get_widget_list()

    def keyPressEvent(self, event):

        super(MainUI, self).keyPressEvent(event)
