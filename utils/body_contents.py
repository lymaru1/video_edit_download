from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QStackedLayout, QHBoxLayout

from utils import lym_log
import logging.config

from utils import body_download, body_cut


class BodyContents(QWidget):
    def __init__(self, parent):
        super(BodyContents, self).__init__(parent)
        self.parent = parent  # 부모 저장
        logging.config.dictConfig(lym_log.LOGGING)
        self.log = logging.getLogger('widget')

        self.base_layout = QHBoxLayout()
        self.contents_stack = QStackedLayout() # 컨텐츠 영역

        self.init_base_layout() # 베이스 레이아웃 설정
        self.make_assign_item() # 컨텐츠 생성 객체 생성

        background = QPalette()  # 창에 색상 적용 가능하게 팔레트 호출
        background.setColor(self.backgroundRole(), QColor(240, 240, 240))    # 창 배경에 적용할 색을 저장
        self.setPalette(background)  # 색상 적용
        self.setAutoFillBackground(True)

    def init_base_layout(self):
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(0)
        self.base_layout.addLayout(self.contents_stack)
        self.setLayout(self.base_layout)

    def make_assign_item(self):
        """
            컨텐츠 객체 생성
        """
        self.video_download = body_download.BodyDownload()
        self.video_download.setObjectName('video_download')
        self.video_cut = body_cut.BodyCut()
        self.video_cut.setObjectName('video_cut')

        self.contents_stack.addWidget(self.video_download)
        self.contents_stack.addWidget(self.video_cut)

    def contents_change(self, widget):
        """
        컨텐츠 스텍에 내용을 변경한다.
        :param widget: 컨텐츠 위젯
        """
        position = self.contents_stack.indexOf(widget)
        if position != -1:
            self.contents_stack.setCurrentIndex(position)

    def contents_get_widget_list(self) -> list:
        """
        바디 컨텐츠에 있는 컨텐츠 목록을 반환해준다.
        :return: 컨텐츠 위젯 리스트
        """
        contents_list: list = []
        # 컨텐츠 목록 추출
        for i in range(self.contents_stack.count()):
            contents_list.append(self.contents_stack.itemAt(i).widget())

        return contents_list
