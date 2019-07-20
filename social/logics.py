

from user.models import User
from social.models import Friend,Swiped
import datetime
from common.cache_key import *
from django.core import cache
from common.errors import *
from common import config




"""
1.我们通过user对象下的perfile来找到我们应该推荐谁
2.因为年龄是18.19之类的数字,但是我们之前的用户是输入年份,所以我们要进行计算
18岁 = 2019 - 2001 
22岁 = 2019 - 1997
通过下面maxyear-minyear  我们要查多少年则可以找出来了

"""
def recommend_users(user):


    today = datetime.date.today()

    max_year = today.year - user.profile.min_dating_age   #这里是当前年份 - 最小匹配的年份(user.model表写的是18岁)

    min_year = today.year - user.profile.max_dating_age   #这里是当前年份 - 最大匹配的年份(user.model表写的是40岁)

    swiped_users = Swiped.objects.filter(uid=user.id).only('sid')  #这个放的是已经被划过的用户.因为被划过,所以不能再重新被划到,uid=我们当前用户的id,我们只需要sid,所以用only函数,只提取sid
    print(swiped_users.query)  # 使用query打印原生的sql语句

    swiped_sid_list = [s.sid for s in swiped_users]   #这是一个列表生成式,将上面的转成列表



    rec_users = User.objects.filter(
        location = user.profile.location,
        sex = user.profile.dating_sex,
        birth_year__gte = min_year,
        birth_year__lte= max_year
      #使用exclude函数将上面的swiped_sid_list过滤掉,不需要,只有过滤掉,才在显示中不会重复显示
    ).exclude(id__in = swiped_sid_list)   #这时候我们导入模型进行查数据,我们根据性别和地理位置查数据
    print(rec_users.query)  #使用query打印原生的sql语句

    return rec_users




# ------------------------------------------------------------------------------

"""
喜欢的操作:
如果被滑动的那个人(也操作了喜欢滑动你用户)喜欢当前滑动的用户.则创建好友关系

"""

def like_someone(uid, sid):


    ret = Swiped.huadong_move(uid=uid, sid=sid, mark ='like')  #单方面滑动动作

    if ret and Swiped.is_liked(sid, uid):  #如果 sid 喜欢 uid ,则进行好友操作(只有你喜欢我我喜欢你才能创建好友关系)

        _, created = Friend.make_friends(sid,uid)    #调用models模型的函数make_friends
        return created
    else:
        return False

        print('+++++++++++++++++我们加个好友吧++++++++++++++++++++++')


# ------------------------------------------------------------------------

"""
超级喜欢的操作:
如果被滑动的那个人(也操作了喜欢滑动你用户)喜欢当前滑动的用户.则创建好友关系

"""


def superlike_someone(uid, sid):

    ret = Swiped.huadong_move(uid=uid, sid=sid, mark='superlike')   #将Swiped.objects.create,全部改成Swiped.huadong_move,改成一个动作了

    if ret and Swiped.is_liked(sid, uid):
        # Friend.make_friends(sid,uid)    #调用models模型的函数make_friends
        _, created = Friend.objects.make_friend(sid,uid)  #这里使用自己定义的管理器方法,不使用上面这个了
        return created
    else:
        return False


def dislike_someone(uid, sid):

    pass


# ---------------------------------------------------------------------------
"""
反悔接口
1.撤销上一次滑动操作的记录
2.撤销上一次创建的好友关系(如果上一步是like或者superlike,我们才要撤销好友关系)

"""

def rewind_someone(user):

    key = SWIPE_LIMIT_PREFIX2.format(user.id)

    swipe_times = cache.get(key,0)  #这样就拿到每日的上限,弄个默认值0次

    if swipe_times >= config.SWIPE_LIMIT:
        raise SwipeLinmitError


    swipe = Swiped.objects.filter(uid=user.id,).latest('created_at')   #通过models字段created_at字段找到最新的记录,这里就一条记录,就是最新那一条
    if swipe.mark in ['like', 'superlike']:
        Friend.del_friendship(swipe.uid,swipe.sid)

    swipe.delete()

    now = datetime.datetime.now()
    timeout = 86400 - now.hour * 3600 + now.minute*60 + now.second
    cache.set(key,swipe_times +1, timeout=timeout)


"""
这个接口用于查看喜欢过我的人,过滤掉已经存在的好友
"""


def like_me_someone(user):

    friend_list = Friend.myself_fidlist(user.id)
    swipe_list = Swiped.objects.filter(sid=user.id,mark__in=['like','superlike']).exclude(uid__in=friend_list).only('uid')  #sid就是我自己  Swiped.objects.filter(sid=user.id)表示查看过我的人,喜欢过我的人

    liked_me_uid_list = [s.uid for s in swipe_list]

    return liked_me_uid_list