from common.utils import is_phone_num
from django.http import JsonResponse
from libs.http import render_json
from user import logics
from common.errors import *
from common.cache_key import *
from django.core.cache import cache
from user.models import User
from libs import orm
from user.forms import ProfileFrom
import time
from django.conf import settings
import os


def verify_phone(request):

    phone_num = request.POST.get('phone_num')

    # if is_phone_num(phone_num):
    #
    #     # logics.send_virify_code(phone_num)
    #     return render_json()
    # else:
    #     return render_json(code=PHONE_NUM_ERROR)


    if is_phone_num(phone_num):

        if logics.send_verify_code(phone_num):
            return render_json()
        else:

            return render_json(code=SMS_SEND_ERR)
    else:
        return render_json(code=PHONE_NUM_ERR)




def login(request):


    phone_num = request.POST.get('phone_num','')
    # phone_num = request.POST.get('phone_num')
    print(phone_num)

    code = request.POST.get('code','')

    phone_num = phone_num.strip()
    code = code.strip()

    cached_code = cache.get(VERIFY_CODE_KEY_PREFIX.format(phone_num))

    if cached_code != code:
        return render_json(code=VERIFY_CODE_ERR)

    user, created = User.objects.get_or_create(phonenum=phone_num)#如果存在记录,则get,否则create

    # 设置登录状态
    request.session['uid'] = user.id

    # 假如是token的话,token的认证方式是,代码如下:(为当前登录用户生成一个token,并且保存到缓存之中,key为:token:user id,Value为:token)
    # token= user.get_or_create_token()
    # data = {'token':token}
    # return render_json(data=data)

    return render_json(data=user.to_dict())



def get_profile(request):


    user = request.user
    # uid = request.session.get('uid')
    # user = User.objects.get(pk=uid)
    return render_json(data=user.profile.to_dict(exclude=['auto_play']))


def change_profile(request):
    user = request.user
    form = ProfileFrom(data=request.POST,instance=user.profile)
#    导入forms.py里面的ProfileFrom实例化, 因为更新,所以要有两个参数
#       data参数:请求的数据   instance参数:实例   将表单的数据更新到实例里面
    if form.is_valid():
        form.save()   #将更改的字段保存,更新到个人
        return render_json()
    else:
        return render_json(data=form.errors)


# -------------------------------------------------------------------------------
def upload_icon(request):

    user = request.user
    avatar = request.FILES.get('avatar')
    logics.yibu_upload_icon.delay(user,avatar)

    return render_json()
    # file_name = 'icon-{}'.format(int(time.time()))#这里不设置扩展名,系统自动识别的.
    #
    # file_path = logics.upload_icon(file_name,icon)
    #
    # ret = logics.upload_qiniuyun(file_name,file_path)
    #
    # if ret:
    #     return render_json()
    # else:
    #     return render_json(ICON_UPLOAD_ERR)
    # # file_path = os.path.join(settings.MEDIA_ROOT,file_name)  #获取文件的路径
    # # with open(file_path,'wb') as destination:
    # #     for chunk in icon.chunks():
    # #         destination.write(chunk)   #chunk方法只有django有,python是没有的

# ------------------------------------------------------------------------------------



