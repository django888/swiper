from common.errors import *
from django.http import JsonResponse

def render_json(code=OK,data=None):

    result = {
        'code': code
    }

    if data:
        result['data'] = data

    json_dumps_params = {
        'separators':(',',':')
    }


    return JsonResponse(data=result,json_dumps_params=json_dumps_params)


        # json_dumps_params = {
        #     'separators': (',', ':')
        # }
        #
        # return JsonResponse(data=result,json_dumps_params=json_dumps_params)