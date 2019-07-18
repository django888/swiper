from django.core.cache import cache

from common import utils, cache_key
from libs import sms,qiniuyun
from django.conf import settings
import os,time
from worker import celery_app


def send_verify_code(phone_num):
    """
    发送验证码逻辑
    :param phone_num: 手机号
    :return:
    """

    # 生成验证码
    code = utils.gen_random_code(6)

    # 发送验证码
    ret = sms.send_virify_code(phone_num, code)

    if ret:
        cache.set(cache_key.VERIFY_CODE_KEY_PREFIX.format(phone_num), code, 60 * 3)

    return ret



def upload_icon(file_name,icon):

    file_path = os.path.join(settings.MEDIA_ROOT,file_name)  #获取文件的路径
    with open(file_path,'wb+') as destination:
        for chunk in icon.chunks():
            destination.write(chunk)   #chunk方法只有django有,python是没有的

    return file_path

def upload_qiniuyun(file_name,file_path):

    ret,info = qiniuyun.upload(file_name,file_path)

    return True if info.status_code == 200 else False



"""
异步上传头像的函数,使用celery,异步上传头像到七牛云
这里的做法是:1.把它声明称celery的一个异步任务
2.异步任务生成文件名,上传到本地
3.再上传到七牛云
"""
@celery_app.task
def yibu_upload_icon(icon):

    file_name = 'icon-{}'.format(int(time.time()))#这里不设置扩展名,系统自动识别的.
    file_path = upload_icon(file_name,icon)#调用上面函数

    upload_qiniuyun(file_name,file_path)#调用上面函数
