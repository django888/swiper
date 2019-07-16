from common.utils import is_phone_num
from django.http import JsonResponse
from libs.http import render_json
from user import logics

from common.errors import *

def verify_phone(request):

    phone_num = request.POST.get('phone_num')

    if is_phone_num(phone_num):
        logics.send_virify_code(phone_num)
        return render_json()
    else:
        return render_json(code=PHONE_NUM_ERROR)
