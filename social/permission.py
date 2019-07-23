from common.errors import VipPermError

def has_perm(perm_name):
    def decorator(view_func):
        def wrapper(request,*args,**kwargs):
            if request.user.vip.has_perm(perm_name):
                return view_func(request,*args,**kwargs)
            else:
                raise VipPermError
        return wrapper

    return decorator