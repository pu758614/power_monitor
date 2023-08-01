import json 
from app import models
from django.utils import timezone
from app.lib.api_lib import apiLib
from datetime import datetime

class syncDataLib():
    
    def __init__(self):
        pass
    
    def syncStationRealKpi(self):
        api_data = apiLib().getStationRealKpi()
        if(len(api_data)>0):
            api_data = api_data[0]
            if('dataItemMap' in api_data):
                kpi_data = api_data['dataItemMap']
                kpi_data_json = json.dumps(kpi_data)
                data = models.config.objects.filter(name='station_real_kpi').first()
                if(data==None):
                    models.config.objects.create(
                        name = 'station_real_kpi',
                        text=kpi_data_json
                    )
                else:
                    models.config.objects.filter(id=data.id).update(
                        text=kpi_data_json,
                        update_time = timezone.now()
                    )

    
    
    def syncDevKpiDay(self):
        data_list = apiLib().getDevKpiDay()
        for data in data_list:
            collect_time = int(data['collectTime'])/1000
            collect_time = datetime.utcfromtimestamp(collect_time).strftime('%Y-%m-%d %H:%M:%S')
            query_data = models.dev_kpi_day.objects.filter(
                collect_time=collect_time,
                dev_id =data['devId']
            ).first()
            if(query_data==None):
                models.dev_kpi_day.objects.create(
                    collect_time=collect_time,
                    dev_id=data['devId'],
                    sn=data['sn'],
                    installed_capacity = data['dataItemMap']['installed_capacity'],
                    product_power = data['dataItemMap']['product_power'],
                    perpower_ratio = data['dataItemMap']['perpower_ratio'],
                )
        return True