

from common import utils
from libs import sms

def send_virify_code(phone_num):
    code = utils.gen_random_code(6)

    sms.send_virify_code(phone_num,code)