import logging
import os
import sys
import traceback
import datetime
from django.conf import settings

def exceptParseMsg(e):
    error_class = e.__class__.__name__  # 取得錯誤類型
    traceback_info = sys.exc_info()  # 取得Call Stack
    last_call_stacks = traceback.extract_tb(
        traceback_info[2])  # 取得Call Stack的最後一筆資料
    stack_msg = ''
    stack_msg_list = []
    for last_call_stack in last_call_stacks:
        file_name = last_call_stack[0]  # 取得發生的檔案名稱
        line_num = last_call_stack[1]  # 取得發生的行號
        func_name = last_call_stack[2]  # 取得發生的函數名稱
        stack_msg_list.append(
            stack_msg+f"{file_name},line {line_num}, in {func_name} {error_class}")
    stack_msg = "\n".join(stack_msg_list)
    return stack_msg


def exceptLog(action_name, e):
    stack_msg = exceptParseMsg(e)
    err_msg = f"[{action_name}] {stack_msg}"
    logFile(err_msg, 'except_log', 'error')
    return err_msg


def logFile(msg, file_name='', level='info'):
    if(file_name==''):
        file_name = getattr(settings, 'PROJECT_NAME')
    logger = setupLogger(file_name, level)

    if (level == 'error'):
        logger.error(msg)
    elif (level == 'debug'):
        logger.debug(msg)
    elif (level == 'warning'):
        logger.warning(msg)
    else:
        logger.info(msg)
    return True


def setupLogger(log_file, level='info'):
    log_dir_root = getattr(settings, 'LOG_DIR_ROOT')
    formatter = logging.Formatter('[%(asctime)s][%(levelname)8s] %(message)s')
    os.makedirs(log_dir_root, exist_ok=True)
    today = datetime.date.today()
    # os.makedirs(f'{log_dir_root}/{today}/', exist_ok=True)
    handler = logging.FileHandler(f'{log_dir_root}/'+log_file+".log")
    handler.setFormatter(formatter)
    if (level == 'error'):
        level = logging.ERROR
    elif (level == 'debug'):
        level = logging.DEBUG
    elif (level == 'warning'):
        level = logging.WARNING
    else:
        level = logging.INFO

    logger = logging.getLogger(__name__)
    if (logger.hasHandlers()):
        logger.handlers.clear()
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
