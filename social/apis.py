from django.shortcuts import render
from libs.http import render_json
from social import logics
from social.models import Swiped
from common.errors import *
from user.models import User
# Create your views here.



# --这是一个  推荐好友列表   的函数/接口---------------------------------------------------------------------------------------------------
"""
1.最后我们输出一堆用户,所以创建user列表,最后的data参数返回列表


"""
def recommend(request):

    user = request.user

    rec_users = logics.recommend_users(user)

    users = [u.to_dict() for u in rec_users]  #这是一堆用户的用户数据,   列表生成式

    return render_json(data=users)




# --这是一个  喜欢我   的函数/接口---------------------------------------------------------------------------------------------------

def like(request):

    user = request.user

    sid = request.POST.get('sid')
    if sid is None:
        return render_json(code='错误啦错误啦,返回你一个错误码')
    sid = int(sid)  #需要将字符串改成整形

    matched = logics.like_someone(user.id,sid)


    return render_json(data={'matched':matched})




# --这是一个  我不喜欢   的函数/接口---------------------------------------------------------------------------------------------------

def dislike(request):
    user = request.user

    sid = request.POST.get('sid')
    if sid is None:
        return render_json(code=SID_ERR)
    sid = int(sid)  #需要将字符串改成整形

    Swiped.huadong_move(uid=user.id,sid=sid,mark='dislike')



    return render_json()

# --这是一个  超级喜欢   的函数/接口---------------------------------------------------------------------------------------------------

def superlike(request):

    user = request.user
    sid = request.POST.get('sid')
    if sid is None:
        return render_json(code=SID_ERR)
    sid = int(sid)

    matched = logics.superlike_someone(user.id, sid)

    return render_json(data={'matched':matched})

# --这是一个  返回接口(就会之前不喜欢,现在更改为喜欢)   的函数/接口---------------------------------------------------------------------------------------------------
"""
反悔接口
1.撤销上一次滑动操作的记录
2.撤销上一次创建的好友关系

"""
def rewind(request):

    user = request.user

    logics.rewind_someone()


    return render_json()

# --这是一个  喜欢我   的函数/接口---------------------------------------------------------------------------------------------------
"""
查看喜欢过我的人,本质上是从记录里面,我是sid的like与superlike动作都找到,找到后
uid就是喜欢过我的人, 谁喜欢我就是uid 而我就是sid
然后把我们已经匹配好友关系的剔除出去

"""




def like_me(request):

    user = request.user

    uid_list = logics.like_me_someone(user)

    users = [u.to_dict() for u in User.objects.filter(id__in=uid_list)]

    return render_json(data=users)

