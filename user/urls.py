
from django.urls import path
from user.views import *
from user.apis import *
urlpatterns = [
    path('app/',index),
    path('verify_phone/',verify_phone),

]