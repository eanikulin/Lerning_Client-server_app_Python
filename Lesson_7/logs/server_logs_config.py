import logging
import sys, os
import yaml

with open('config.yaml', encoding='utf-8') as conf_file:
    data = yaml.load(conf_file, Loader=yaml.FullLoader)

LOG_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), data['LOG_DIRECTORY'])
LOG_FILE = os.path.join(LOG_DIRECTORY, data['LOG_SERVER_NAME'])


logger = logging.getLogger('server')
logger.setLevel(logging.DEBUG)

format_log = logging.Formatter('%(asctime)-10s %(levelname)-10s %(filename)-10s %(message)s')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(format_log)

file_handler = logging.FileHandler(LOG_FILE)
# file_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, encoding='utf-8', when='D', interval=1,
#                                                          backupCount=7)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(format_log)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

if __name__ == '__main__':
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
    logger.warning('Внимание')
