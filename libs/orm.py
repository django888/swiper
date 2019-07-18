




#
# def get_profile(request):
#     user = request.user
#
#     return render_json(data=user.profile)
#

# 上面的是apri.py里面的函数, return render_json(data=user.profile),
# 里面的data必须是字典类型,为了避免每次都去像model.py里面的函数一样def to_dict(self):
# 每一次都去转字典类型,所以就定义一个类,
class ModelToDictMixin():
    def to_dict(self,exclude=[]):
        attr_dict = {}
        fields = self._meta.fields#model所有字段的属性

        for field in fields:
            field_name = field.attname
            if field_name not in exclude:
                attr_dict[field_name] = getattr(self,field_name)

        return attr_dict