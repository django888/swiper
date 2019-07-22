

"""
业务状态码、错误码
"""

OK = 0

# 系统保留状态码
# 1000 - 1999


# 用户系统
# 2000 - 2999
PHONE_NUM_ERR = 2001        # 手机号格式错误
SMS_SEND_ERR = 2002         # 验证码发送失败
VERIFY_CODE_ERR = 2003      # 验证码错误

LOGIN_REQUIRED_ERR = 2004   #用户认证错误

ICON_UPLOAD_ERR = 2005      #七牛云上传失败



# 社交模块开发的错误码
SID_ERR = 3001           #SID参数错误
HUADONG_ERR = 3002       #滑动动作错误异常



MISTAKE = {
    '1002':'XXX错误',
    '1003':'SSS错误',
}

"""
自定义异常处理
调用者通过参数,传递出去错误码

"""
class LogicException(Exception):
    def __init__(self,code):

        self.code = code

# --------------------------------------------------------------------------

class LogsicErr(Exception):
    code = None

def logic_error(name,code):
    return type(name,(LogsicErr,),{'code':code})


SidError = logic_error('Sid有错误啦',3001)
HuaDongError = logic_error('你滑动的方式错误了啦',3002)
SwipeLinmitError = logic_error('超过上限的错误',3003)        #超过次数的限制了



# VIP系统错误

# VipPermError = logic_error()

