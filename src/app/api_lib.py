import requests


class apiLib():
    
    def __init__(self):
        self.user_name = "chenhousespvsys"
        self.system_code = "00000aaa"
        self.domain = "00000aaa"
        self.token = 'https://intl.fusionsolar.huawei.com'
        
    def login(self):
        url = f"{self.domain}/thirdData/login"
        data = {
            "userName":self.user_name,
            "systemCode":self.domain 
        }
        response = requests.post(url, data=data)
        
        


    

    