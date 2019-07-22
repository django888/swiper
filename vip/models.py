from django.db import models

# Create your models here.

class Vip(models.Model):
    level = models.IntegerField(default=0,verbose_name='等级',unique=True)
    name = models.CharField(max_length=128,verbose_name='会员姓名',unique=True)

    price = models.DecimalField(max_digits=5,decimal_places=2,default=0,verbose_name='价钱')

    class Meta:
        db_table = 'vips'


class Permission(models.Model):
    name = models.CharField(max_length=32,unique=True)
    description = models.CharField(max_length=600)   #给用户看的会员功能描述


    class Meta:
        db_table = 'permissions'


class VipPermission(models.Model):   #多对多关系表
    vip_id = models.IntegerField(verbose_name='会员id')
    perm_id = models.IntegerField(verbose_name='权限id')

    class Meta:
        db_table = 'vip_permissions'

