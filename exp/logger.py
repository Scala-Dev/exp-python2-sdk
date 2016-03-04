
import logging
from logging.handlers import RotatingFileHandler


_file_handler_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
_file_handler = RotatingFileHandler('debug.log', mode='a', maxBytes=5*1024*1024, backupCount=5, encoding=None, delay=0)
_file_handler.setFormatter(_file_handler_formatter)
_file_handler.setLevel(logging.DEBUG)

_stream_handler_formatter = logging.Formatter('EXP/%(levelname)-10s: %(message)s')
_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(logging.INFO)
_stream_handler.setFormatter(_stream_handler_formatter)

logger = logging.getLogger('exp')
logger.addHandler(_file_handler)
logger.addHandler(_stream_handler)
logger.setLevel(logging.DEBUG)
