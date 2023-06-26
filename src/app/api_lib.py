import requests
import json 


class apiLib():
    
    def __init__(self):
        self.user_name = "chenhousespvsys"
        self.system_code = "00000aaa"
        self.domain = "https://intl.fusionsolar.huawei.com"
        self.mock = False
        self.token = self.login()
        
    
    def getLoginToken(self):
        pass
    
    def stations(self,page=1,page_size=50):
        url = f"{self.domain}/thirdData/stations"
        data = {
            "pageNo":page,
            "pageSize":page_size
        }
        json_data = json.dumps(data) 
        headers = {
            'xsrf-token':self.token
        }
        print(headers)
        response = requests.post(url, json=data,headers=headers)
        if(response.status_code==200):
            data = response.text

        
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
        

        
        


    

    