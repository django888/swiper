


import re
import random

PHONE_PATTERN = re.compile(r'^1[3-9]\d{9}$')

def is_phone_num(phone_num):

    # if PHONE_PATTERN.match(phone_num):
    #     return True
    # else:
    #     return False

    return True if PHONE_PATTERN.match(phone_num.strip()) else False


def gen_random_code(length = 4):

    if not isinstance(length,int):
        length = 1

    if length <=0:
        length = 1

    code = random.randrange(10**(length-1),10**length)
    return str(code)