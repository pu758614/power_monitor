from django.http import HttpResponse
import json
from django.core.paginator import Paginator
import time
import pytz
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from library.check_formate import checkFormateClass
import socket


def emptyDefault(val, default):
    if (checkFormateClass().isEmpty(val)):
        val = default
    return val


def checkPortIsOpen(port, ip='127.0.0.1'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))  # 連結成功返回0
    if result == 0:
        return True
    else:
        return False


def paginationInfo(query_list, page, count):
    data_list = query_list
    pagination = {
        "total": len(query_list),
        "current_page": 1,
        "total_page": 1,
        "has_pre": False,
        "pre_page": 0,
        "has_next": False,
        "next_page": 0
    }
    if (checkFormateClass().isEmpty(query_list)):
        pagination = {
            "total": len(query_list),
            "current_page": 0,
            "total_page": 0,
            "has_pre": False,
            "pre_page": 0,
            "has_next": False,
            "next_page": 0
        }
    elif (checkFormateClass().isEmpty(count) == False):
        page = int(page)
        count = int(count)
        data_list = {}
        if (page != 0 and count != 0):
            paginator = Paginator(query_list, count)
            if (paginator.num_pages >= page):
                data_list = paginator.page(number=page)
                try:
                    pre_page = data_list.previous_page_number()
                except:
                    pre_page = 0
                try:
                    next_page = data_list.next_page_number()
                except:
                    next_page = 0
                pagination = {
                    "total": len(query_list),
                    "current_page": data_list.number,
                    "total_page": paginator.num_pages,
                    "has_pre": data_list.has_previous(),
                    "pre_page": pre_page,
                    "has_next": data_list.has_next(),
                    "next_page": next_page
                }

    return {
        "pagination": pagination,
        "data_list": data_list
    }


def isRequestAdmin(request):
    result = False
    try:
        result = request.user.has_perm('permission.admin')
    except Exception as e:
        pass
    return result


def getClientIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def localNow(type='time'):
    return localTime(timezone.now(), type)


def localTime(date_time='', t_type='time'):
    time_zone = getattr(settings, 'TIME_ZONE')
    local_dt = timezone.localtime(date_time, pytz.timezone(time_zone))
    if (t_type == 'date'):
        date_time = local_dt.strftime("%Y-%m-%d")
    elif (t_type == 'stamp'):
        date_time = time.mktime(datetime.strptime(local_dt.strftime(
            "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S").timetuple())
    else:
        date_time = local_dt.strftime("%Y-%m-%d %H:%M:%S")
    return date_time


def convertStrToTime(original_datetime, fmt='%Y-%m-%d %H:%M:%S'):
    new_datetime = datetime.strptime(original_datetime, fmt)
    tz = timezone.get_current_timezone()
    timezone_datetime = timezone.make_aware(new_datetime, tz, True)
    return timezone_datetime


def getMytimezoneDateTime(original_datetime):
    new_datetime = datetime.strptime(original_datetime, '%Y-%m-%d %H:%M:%S.%f')
    tz = timezone.get_current_timezone()
    timezone_datetime = timezone.make_aware(new_datetime, tz, True)
    return timezone_datetime


def apiResponse(error=1, data={}, msg='', http_status_code=200):
    if (error != 0 and msg == '' and str(type(data)) == "<class 'str'>"):
        msg = data
        data = {}
    result = {
        'error': error,
        'msg': msg,
        'data': data
    }
    response = HttpResponse(json.dumps(result), status=http_status_code)
    return response
