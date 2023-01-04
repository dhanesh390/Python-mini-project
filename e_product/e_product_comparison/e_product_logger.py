import logging

logger = logging.getLogger(__name__)
stream_log_handler = logging.StreamHandler()
file_log_handler = logging.FileHandler("e_product_comparison.log")
stream_log_handler.setLevel(logging.DEBUG)
file_log_handler.setLevel(logging.DEBUG)
stream_log_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_log_handler.setFormatter(stream_log_format)
file_log_handler.setFormatter(file_log_format)
logger.addHandler(stream_log_handler)
logger.addHandler(file_log_handler)

