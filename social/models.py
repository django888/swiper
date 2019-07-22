from django.db import models
from django.db.models import Q
from social.managers import FriendManager
from common.errors import *

# Create your models here.

class Swiped(models.Model):#这个表是记录划过的人的每一次操作记录
    MARKS = [
        ('like','喜欢'),
        ('dislike', '不喜欢'),
        ('superlike', '超级喜欢'),
    ]

    uid = models.IntegerField(verbose_name='登陆者的id')
    sid = models.IntegerField(verbose_name='被划过/被喜欢的人')
    mark = models.CharField(max_length=16,choices=MARKS,verbose_name='使用动作的标记')  #choise参数表示这是一个选项

    created_at = models.DateTimeField(auto_now_add=True,verbose_name='使用动作的时间')


    """
      这个动作主要是为了创建一个滑动的记录
    如果已经在数据库查到了这个动作已经存在,返回False
    否则(没有这个动作),创建一条新的记录,然后返回True
    为的就是限制滑动次数,不能一个人滑动两次
    """
    @classmethod
    def huadong_move(cls,uid,sid,mark):   #包装成一个动作

        marks = [m for m,_ in cls.MARKS] #这里的m代表like  下划线代表喜欢,但是我们这里只取like/superlike/dislike
        if mark not in marks:  #这是个进行错误处理,不在的话抛出异常
            # raise LogicException(HUADONG_ERR)    封装了,改成下面的用法
            raise HuaDongError


        # cls.objects.update_or_create(uid=uid,sid=sid,mark=mark)   #这行代码用于假如我们mark不止三个选项,增加选项的话,则需要这个代码

        if cls.objects.filter(uid=uid,sid=sid,mark=mark).exists():
            return False
        else:
            cls.objects.create(uid=uid, sid=sid, mark=mark)



    @classmethod
    def is_liked(cls, uid, sid):
        return cls.objects.filter(uid=uid,sid=sid,mark__in=['like','superlike']).exists()


    class Meta:
        db_table = 'swiper'


# --------------------------------------------------------------------------------------

"""
1.其实我们应该设置uid 与 fid 但是因为这两个反应不了他们两个的关系,所以我们这里用uid1跟uid2
因为我们可能是喜欢别人,也可以被别人喜欢.
例如  1    12    我喜欢别人
     12    1    别人喜欢我
     那么表达的方式就是先排序,再去重,弄成一份表

"""

class Friend(models.Model):       #这是一个双向好友关系表   此业务为双向关系,就是你喜欢我,我也喜欢你,  两个字段关联的是唯一的

    uid1 = models.IntegerField()
    uid2 = models.IntegerField()
    objects = FriendManager()

    """
    建立好友关系...通过自定义  uid 排序规则,来组织好友关系,且一组好友关系只保存一份数据
    """
    @classmethod
    def make_friends(cls,uid1,uid2):   #这个是限制无论1-12或者 12-1,都只是会存一条数据
        uid1,uid2 = (uid1,uid2) if uid1 <uid2 else (uid2,uid1)
        return cls.objects.get_or_create(uid1=uid1,uid2=uid2)

    @classmethod
    def del_friendship(cls, uid1, uid2):  # 这个是限制无论1-12或者 12-1,都只是会存一条数据
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)

        return cls.objects.filter(uid1=uid1, uid2=uid2).delete()


    @classmethod
    def myself_fidlist(cls,uid):  #查看我的好友列表
        friend_list = []
        friends = cls.objects.filter(Q(uid1=uid) | Q(uid2=uid))

        for f in friends:
            fid = f.uid1 if uid == f.uid2 else f.uid2
            friend_list.append(fid)

        return friend_list









    class Meta:
        db_table = 'friends'

