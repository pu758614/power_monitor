import requests
import json 
from app import models
from django.utils import timezone

class apiLib():
    
    def __init__(self):
        self.user_name = "chenhousespvsys"
        self.system_code = "00000aaa"
        self.domain = "https://intl.fusionsolar.huawei.com"
        self.mock = False
        self.station_code = 'NE=34005083'
        self.token = self.getLoginToken()
        
    
    def getLoginToken(self):
        data=models.config.objects.filter(
            name='login_token',
        ).first()
       
        if(data==None):
            token=self.login()
            models.config.objects.create(
                name='login_token',
                value = token,
            )
        else:
            diff_time = (timezone.now()-data.update_time).seconds
            if(diff_time>300):
                token = self.login()
                models.config.objects.filter(
                    name='login_token',
                ).update(
                    value = token,
                    update_time = timezone.now()
                )
            else:
                token = data.value
        return token
    
    def getDevKpiDay(self):
        url = f"{self.domain}/thirdData/getDevKpiDay"
        data = {
            "sns":"HV2250306978,HV2250306992,HV2250306925",
            "devTypeId":38,
            "collectTime":1686535200000
        }
        headers = {
            'xsrf-token':self.token
        }
        response = requests.post(url, json=data,headers=headers)
        data = {}
        if(response.status_code==200):
            response_json = response.text
            response_data = json.loads(response_json)
            if('data' in response_data):
                data = response_data['data']
        return data 
    
    
    def getStationRealKpi(self):
        url = f"{self.domain}/thirdData/getStationRealKpi"
        data = {
            "stationCodes":self.station_code,
        }
        headers = {
            'xsrf-token':self.token
        }
        response = requests.post(url, json=data,headers=headers)
        data = {}
        if(response.status_code==200):
            response_json = response.text
            response_data = json.loads(response_json)
            if('data' in response_data):
                data = response_data['data']
        return data        
        
    def stations(self,page=1,page_size=50):
        url = f"{self.domain}/thirdData/stations"
        data = {
            "pageNo":page,
            "pageSize":page_size
        }
        headers = {
            'xsrf-token':self.token
        }
        response = requests.post(url, json=data,headers=headers)
        data = {}
        if(response.status_code==200):
            response_json = response.text
            response_data = json.loads(response_json)
            if('data' in response_data):
                data = response_data['data']
        return data

        
    def login(self):
        if(self.mock==False):
            url = f"{self.domain}/thirdData/login"
            data = {
                "userName":self.user_name,
                "systemCode":self.system_code 
            }
            json_data = json.dumps(data) 

            response = requests.post(url, json=data)
            token = ''
            if(response.status_code==200):
                response_data = response.json()
                if(response_data['success']==True):
                    token = response.headers['xsrf-token']
        else:
            token = 'x-ip5hmq3ytijvbyg447qoqkg7qojxhg6p9cendd9fg7hderdcdi09bzcbbtsb45s5jyilqpsajyc47wimtimn88fv9i2p2kapkb1d3vrxs47uimfuntsaqqk6nwld7sqq'
        return token
        

        
        


    

    