import pprint
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import vlc
from app import models
import json

def dashboard(request):
  
    data_list = models.dev_kpi_day.objects.filter().order_by('-collect_time')
    dev_list = []
    for data in data_list:
        if(data.dev_id not in dev_list):
            dev_list.append(data.dev_id)
    first_data = data_list.first()
    
    station_real_kpi_query=models.config.objects.filter(name='station_real_kpi').first()
    month_power = total_power = day_power = ''
    if(station_real_kpi_query!=''):
        station_real_kpi_data =json.loads(station_real_kpi_query.text)
        month_power = station_real_kpi_data['month_power']
        total_power = station_real_kpi_data['total_power']
        day_power = station_real_kpi_data['day_power']
    
    data_list = models.dev_kpi_day.objects.filter().order_by('collect_time')[0:30]
    curve_line_data = []
    curve_line_days = []
    for data in data_list:
        collect_time = str(data.collect_time)
        collect_time_arr = collect_time.split(" ")
        curve_line_data.append(data.product_power)
        curve_line_days.append(collect_time_arr[0])
    
    curve_line_data_str = json.dumps(curve_line_data)
    curve_line_days_str = json.dumps(curve_line_days)
    context ={
        "dev_list":dev_list,
        "first_div_id":first_data.dev_id,
        "month_power":month_power,
        "total_power":total_power,
        "day_power":day_power,
        "curve_line_data_str":curve_line_data_str,
        "curve_line_days_str":curve_line_days_str,
    }
    return render(request, 'dashboard.html', context)

def stream_rtsp(request):
    # 创建一个VLC实例
    instance = vlc.Instance('--no-xlib')  # 非GUI模式
    player = instance.media_player_new()

    # 设置RTSP URL
    rtsp_url = "rtsp://monitor:1qazxsw2@192.168.2.9:554/main_7"

    # 创建一个媒体对象
    media = instance.media_new(rtsp_url)

    # 将媒体对象与播放器关联
    player.set_media(media)

    # 开始播放
    player.play()

    # 在响应中发送视频流
    def generate():
        while True:
            # 从播放器中提取视频帧
            frame, _, _ = player.video_get_frame()

            # 将帧数据作为响应的一部分发送给客户端
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tostring() + b'\r\n\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

def stream_view(request):
    rtsp_url = "rtsp://monitor:1qazxsw2@192.168.2.9:554/main_7"
    vlc_instance = vlc.Instance()
    media_player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(rtsp_url)
    media_player.set_media(media)
    media_player.play()

    context = {
        'media_player': media_player,
    }
    return render(request, 'stream.html', context)