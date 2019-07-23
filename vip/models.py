from django.db import models

# Create your models here.

class Vip(models.Model):   #这个是会员表
    level = models.IntegerField(default=0,verbose_name='等级',unique=True)
    name = models.CharField(max_length=128,verbose_name='会员姓名',unique=True)

    price = models.DecimalField(max_digits=5,decimal_places=2,default=0,verbose_name='价钱')
    #     双精度:price decimal(5,2) 一共有五个数字,小数点后面占两位 最大数字为999.99

    @property
    def perms(self):
        if not hasattr(self,'_perms'):
            vip_perms = VipPermission.objects.filter(vip_id=self.id).only('perm_id')
            perms_id_list = [p.perm_id for p in vip_perms]

            self._perms = Permission.objects.filter(id__in=perms_id_list)
        return self._perms

    def has_perm(self,perm_name):
        # vip_perms = VipPermission.objects.filter(vip_id=self.id).only('perm_id')
        # perms_id_list = [p.perm_id for p in vip_perms]
        #
        # perms = Permission.objects.filter(id__in=perms_id_list)
        perm_names = [p.name for p in self.perms]

        return perm_name in perm_names


    class Meta:
        db_table = 'vips'


class Permission(models.Model):  #这个是权限表
    name = models.CharField(max_length=32,unique=True)  #存的就是动作,like/superlike/dislike
    description = models.CharField(max_length=600)   #给用户看的会员功能描述


    class Meta:
        db_table = 'permissions'


class VipPermission(models.Model):   #多对多关系表   权限关系表  会员与权限(多对多关系表就是两个关系表的外键)
    vip_id = models.IntegerField(verbose_name='会员id')
    perm_id = models.IntegerField(verbose_name='权限id')

    class Meta:
        db_table = 'vip_permissions'

