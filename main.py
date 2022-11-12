import sys, os, signal
import index
from utils import lym_log
import logging.config
from PySide6.QtWidgets import QApplication

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    if os.path.isdir('logs') is False:
        os.mkdir('logs')

    logging.config.dictConfig(lym_log.LOGGING)
    app_log = logging.getLogger('editor')

    app = QApplication(sys.argv)

    screen = QApplication.primaryScreen()   # 모니터 정보 받아옴
    monitor_width: float = screen.availableSize().width() * screen.devicePixelRatio()   # 모니터 가로 크기
    monitor_height: float = screen.availableSize().height() * screen.devicePixelRatio() # 모니터 세로 크기

    ex = index.MainUI(monitor_width, monitor_height)
    ex.show()
    sys.exit(app.exec())
