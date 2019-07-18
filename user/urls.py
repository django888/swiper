
from django.urls import path
from user.views import *
from user.apis import *
urlpatterns = [
    path('app/',index),
    path('verify-phone/',verify_phone),
    path('login/',login),
    path('get_profile',get_profile),
    path('change_profile',change_profile),
    path('upload_icon',upload_icon),


]