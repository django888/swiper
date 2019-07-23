import datetime

from django.db import models
from django.core.cache import cache
from libs import orm
from vip.models import Vip

# Create your models here.



SEXS = (
        (0,'未知'),
        (1,'男'),
        (2,'女')
    )

LOCATIONS = (
        ('gz','广州'),
        ('bj', '北京'),
        ('sz', '深圳'),
        ('hz', '杭州'),
        ('cd', '成都'),
        ('sh', '上海'),

    )


class User(models.Model):

    phonenum = models.CharField(max_length=32,unique=True,verbose_name='手机号码')
    nickname = models.CharField(max_length=20,verbose_name='昵称')
    sex = models.IntegerField(choices=SEXS,default=0,verbose_name='性别')
    birth_year = models.IntegerField(default=2000,verbose_name='出生年')
    birth_month = models.IntegerField(default=1,verbose_name='出生月')
    birth_day = models.IntegerField(default=1,verbose_name='出生日')
    avatar = models.CharField(max_length=256,verbose_name='头像')
    location = models.CharField(max_length=16, choices=LOCATIONS,default='gz',verbose_name='你的城市')

    vip_id = models.IntegerField(default=1)  #这个自己要看看存的差别


    @property
    def age(self):
        today = datetime.date.today()
        birthday = datetime.date(self.birth_year,self.birth_month,self.birth_day)

        return (today - birthday).days //365


    @property
    def vip(self):
        if not hasattr(self,'_vip'):
            self._vip = Vip.objects.get(pk=self.vip_id)

        return self._vip






    @property
    def profile(self):

        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(pk=self.id)#手动创建1对1关系,两个表的id关联


        return self._profile

    def to_dict(self):

        return {
            'uid': self.id,
            'phonenum':self.phonenum,
            'nickname':self.nickname,
            'sex':self.sex,
            'avatar':self.avatar,
            'location':self.location,
            'age':self.age

        }

    # 为用户生成唯一的token
    # def get_or_create_token(self):
    #     key = 'token:{}'.format(self.id)
    #     token = cache.get(key)  先获取token
    #     if not token:
    #         token = 'token***************kahdkejhjkdhkjha'
    #         cache.set(key, token, 24*60*60)
    #         cache.set(token, uid, 24*60*60)

    #     return token

    class Meta:
        db_table = 'user'


# -------------------------------------------------------------------------------------
class Profile(models.Model,orm.ModelToDictMixin):#这里绑定了两个类
    location = models.CharField(max_length=16, choices=LOCATIONS,default='gz',verbose_name='交友城市')
    min_diatance = models.IntegerField(default=0,verbose_name='寻找的最小公里')
    max_diatance = models.IntegerField(default=10,verbose_name='寻找的最大公里')
    min_dating_age = models.IntegerField(default=18,verbose_name='匹配最小年龄')
    max_dating_age = models.IntegerField(default=40,verbose_name='匹配最大年龄')
    dating_sex = models.IntegerField(choices=SEXS,default=0,verbose_name='喜好的性别')

    auto_play = models.BooleanField(default=True,verbose_name='小动画')

    class Meta:
        db_table = 'profiles'






