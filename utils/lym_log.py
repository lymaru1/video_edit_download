# logging setting
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 기존 로거 비활성화

    # 포맷터
    'formatters': {
        'format1': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y/%m/%d-%H:%M:%S'
        },
        'format2': {
            'format': '%(levelname)s %(message)s'
        },
    },

    # 핸들러
    'handlers': {
        # 로그 파일을 만들어 텍스트로 로그레코드 저장
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/wicly.log',
            'when': "midnight",  # 매 자정마다.
            'formatter': 'format2',
        },
        # 콘솔(터미널)에 출력
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'format1',
        }
    },

    # 로거
    'loggers': {
        'editor': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
        'widget': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
        }
    },
}