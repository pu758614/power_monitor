
import re
import json
import uuid
# import magic
import os
from dateutil.parser import parse


class checkFormateClass:
    def __init__(self):
        self.emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.telRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def isFile(self, data):
        if (self.isEmpty(data)):
            return False
        if (str(type(data))[0:25] != "<class 'django.core.files"):
            return False
        return True

    def isUuid(self, data, uuid_ver=4):
        if (self.isEmpty(data)):
            return False
        try:
            return uuid.UUID(data).version == uuid_ver
        except ValueError:
            return False

    def isEmpty(self, data):
        if (data == None):
            return True
        if (self.isString(data)):
            data = data.lstrip()
            if (data == ''):
                return True
            else:
                return False
        elif (self.isList(data) and len(data) == 0):
            return True
        elif (self.isDict(data) and len(data) == 0):
            return True
        elif (data == 0):
            return True
        else:
            return False

    def isInt(self, data):
        data = str(data)
        if (data[0] == '-' or data[0] == '+'):
            return data[1:].isdigit()
        else:
            return data.isdigit()

    def isFloat(self, numStr):
        flag = False
        numStr = str(numStr).strip().lstrip(
            '-').lstrip('+')    # 去除正数(+)、负数(-)符号
        try:
            reg = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
            res = reg.match(str(numStr))
            if res:
                flag = True
        except Exception as ex:
            pass
        return flag

    def isNumber(self, num):
        if (self.isFloat(num) == True or self.isInt(num) == True):
            return True
        return False

    def isString(self, data):
        if (str(type(data)) == "<class 'str'>"):
            return True
        else:
            return False

    def isList(self, data):
        if (str(type(data)) == "<class 'list'>"):
            return True
        else:
            return False

    def isDict(self, data):
        if (str(type(data)) == "<class 'dict'>"):
            return True
        else:
            return False

    def isEmail(self, data):
        if (re.fullmatch(self.emailRegex, data)):
            return True
        else:
            return False

    def isTelPhone(self, data):
        if (re.fullmatch(self.telRegex, data)):
            return True
        else:
            return False

    def isJson(self, data):
        result = True
        try:
            json.loads(data)
        except:
            result = False
        return result

    def isset(self, arr, key):
        result = True
        try:
            arr[key]
        except:
            result = False
        return result

    def isDateTimeStr(self, str):
        try:
            parse(str)
            return True
        except Exception:
            return False

    def getFileType(self, file):
        file_type = ''
        if (self.isString(file) and os.path.isfile(file)):
            content_type = magic.from_file(file, mime=True)
        try:
            content_type = file.content_type
        except Exception as e:
            pass

        img_conf = [
            'image/png',
            'image/jpeg',
            'image/bmp',
            'image/gif'
        ]

        if (content_type == 'application/pdf'):
            file_type = 'pdf'
        elif (content_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation'):
            file_type = 'pptx'
        elif (content_type == 'application/vnd.ms-powerpoint'):
            file_type = 'ppt'
        elif (content_type in img_conf):
            file_type = 'img'
        elif (content_type == 'application/msword'):
            file_type = 'doc'
        elif (content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
            file_type = 'docx'
        return file_type
