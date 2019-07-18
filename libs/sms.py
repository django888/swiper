
import requests
from common import config
from django.conf import settings


def send_virify_code(phone,code):

    if settings.DEBUG:
        print('send_virify_code:',phone,code)
        return True


    params = config.YZX_SMS_PARAMS.copy()

    params['mobile'] = phone
    params['param'] = code

    resp = requests.post(config.YZX_SMS_URL,json=params)
    print(resp.json())

    if resp.status_code == 200:
        ret = resp.json()
        if ret.get('code') =='000000':
            return True
    return False