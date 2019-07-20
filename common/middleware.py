from django.utils.deprecation import MiddlewareMixin

from libs.http import render_json
from common.errors import *
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):

        WHITE_LIST = [
            'api/user/verify-phone/',
            'api/user/login'
        ]

        if request.path in WHITE_LIST:
            return
        uid = request.session.get('uid')

        if not uid:
            return render_json(code=LOGIN_REQUIRED_ERR)

        request.user = User.objects.get(pk=uid)
#         上面这个是应用在apis.py里面get_profish和change_profile里面的,
#          两个函数都要用这个,以下代码为复杂的写,如果不像上面那样写,就要写成,代码如下
#         uid = request.session.get('uid')   注意这里是session,不是使用POST
#         user = User.objects.get(pk=uid)




#         真实工作中如果ios或者安卓是没有session的,只能用token,代码如下

        # for k,v in request.META.items():
        #     print(k,v)
        #
        # token = request.META.get('HTTP_X_SWIPER_AUTH_TOKEN')  #除了HTTP以外其他的随便修改
        # uid = cache.get(token)
        #
        # if not token:
        #     return render_json(code=LOGIN_REQUIRED_ERR)
        # request.user = User.objects.get(pk=uid)


# -----------------------------------------------------------------------------------------
"""
定义一个中间件
isinstance用法

a = 1   type(a) 等于int类型   isinstance(a,int) 返回一个True 表示a是int类型
用法跟之前type(a) == int 这样也是返回True  用上方用法,不用这个
"""
class LogicExceptionMiddleware(MiddlewareMixin):
    def process_exception(self,request,exception):  #函数的名字是固定的,request所有中间件都必须接受的参数,exception:异常的实例,然后下面进行处理
        if isinstance(exception,(LogicException,LogsicErr)):                 #我们怎么判断一个实例是某一个类的类型,如果exception是LogicException类型
            return render_json(code=exception.code)  #这样我们能把异常处理掉,然后很友好的抛到前端

