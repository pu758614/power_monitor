from rest_framework.views import APIView
from rest_framework.decorators import api_view
from app import models
from rest_framework.response import Response
from library import lib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(["POST"])
def getCurveLineData(request):
    dev_id = request.data.get('dev_id','')
    data_list = models.dev_kpi_day.objects.filter(dev_id=dev_id).order_by('-collect_time')[0:29]
    curve_line_data = []
    curve_line_days = []
    point_radius=[]
    point_hover_radius=[]
    point_background_color = []
    point_border_color =[]
    for data in data_list:
        collect_time = str(data.collect_time)
        collect_time_arr = collect_time.split(" ")
        curve_line_data.append(data.product_power)
        curve_line_days.append(collect_time_arr[0])
        point_radius.append(4)
        point_hover_radius.append(2)
        point_background_color.append("#1F3BB3")
        point_border_color.append("#fff")
    curve_line_data.reverse()
    curve_line_days.reverse()
    return_data = {
        "curve_line_data":curve_line_data,
        "curve_line_days":curve_line_days,
        "point_radius":point_radius,
        "point_hover_radius":point_hover_radius,
        "point_background_color":point_background_color,
        "point_border_color":point_border_color,
    }
    return lib.apiResponse(0,return_data)

@api_view(["POST"])
def getDevKpiDayList(request):
    page = request.data.get('page',1)
    count = request.data.get('count',10)
    dev_id = request.data.get('dev_id','')
    
    query_data=models.dev_kpi_day.objects.filter(
        dev_id=dev_id
    ).order_by('-collect_time')
    page_data = lib.paginationInfo(query_data,page,count)
    query_list = page_data['data_list']
    data_list = []
    no = 1
    for data in query_list:
        # collect_time = lib.localTime(data.collect_time,'date')
        collect_time = str(data.collect_time)
        collect_time_arr = collect_time.split(" ")
        data_list.append({
            "no":(page-1)*count+no,
            "dev_id":data.dev_id,
            "collect_time":collect_time_arr[0],
            "sn":data.sn,
            "installed_capacity":data.installed_capacity,
            "product_power":data.product_power,
            "perpower_ratio":data.perpower_ratio,
        })
        no = no+1
 
    return lib.apiResponse(0,{"data":data_list,"page_info":page_data['pagination']})
    