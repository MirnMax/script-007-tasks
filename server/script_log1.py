import logging

logger_ex = logging.getLogger('[Exception_logger]')
logger_info = logging.getLogger('[Data_logger]')
logger_ex.setLevel(logging.ERROR)
logger_info.setLevel(logging.INFO)



s_handler = logging.StreamHandler()
ex_f_handler = logging.FileHandler('ex_file.log')
data_f_handler = logging.FileHandler('data_file.log')


common_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -  %(message)s')
s_handler.setFormatter(common_format)
ex_f_handler.setFormatter(common_format)
data_f_handler.setFormatter(common_format)

# Add handlers to the logger_obj
logger_ex.addHandler(s_handler)
logger_ex.addHandler(ex_f_handler)

logger_info.addHandler(s_handler)
logger_info.addHandler(data_f_handler)

logger_ex.debug("This is a harmless debug Message")
logger_ex.info("This is just an information")
logger_ex.warning("It is a Warning. Please make changes")
logger_ex.error("You are trying to divide by zero")
logger_ex.critical("Internet is down")

logger_info.debug("This is a harmless debug Message")
logger_info.info("This is just an information")
logger_info.warning("It is a Warning. Please make changes")
logger_info.error("You are trying to divide by zero")
logger_info.critical("Internet is down")
