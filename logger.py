import logging

log_file = 'yt_dlp_log.txt'
logging.basicConfig(
    level=logging.DEBUG,  # Capture all levels of logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file,
    filemode='a'  # 'a' for append, 'w' for overwrite
)

class YTDLPPyLogger:
    def debug(self, msg):
        logging.debug(msg)

    def info(self, msg):
        logging.info(msg)

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

    def critical(self, msg):
        logging.critical(msg)