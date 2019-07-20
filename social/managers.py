"""
"""
"""
通过管理器来扩展类方法
自定义管理器

"""

from django.db import models



class FriendManager(models.Manager):  #这里设置成Manager,不设置成Models,因为把他改成类方法
    def make_friends(self,uid1,uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return self.get_or_create(uid1=uid1, uid2=uid2)  #这里删除掉了objects,因为self本来就是一个类方法
