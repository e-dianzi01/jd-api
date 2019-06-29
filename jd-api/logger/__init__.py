import logging
from logging.handlers import TimedRotatingFileHandler

api_logger = logging.getLogger('api_logger')
api_logger.setLevel(logging.DEBUG)


fmt_str = "[%(asctime)s at %(lineno)s line of %(filename)s ] %(message)s"
formatter = logging.Formatter(fmt=fmt_str,
                              datefmt='%Y-%m-%d %H:%M:%S')

handler1 = logging.StreamHandler()
handler1.setLevel(logging.DEBUG)
handler1.setFormatter(formatter)

handler2 = TimedRotatingFileHandler('api-info.log', interval=2, encoding='utf-8')
handler2.setLevel(logging.INFO)
handler2.setFormatter(formatter)

handler3 = TimedRotatingFileHandler('api-error.log', interval=4, encoding='utf-8')
handler3.setLevel(logging.ERROR)
handler3.setFormatter(formatter)

api_logger.addHandler(handler1)
api_logger.addHandler(handler2)
api_logger.addHandler(handler3)