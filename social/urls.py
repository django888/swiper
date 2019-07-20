from django.urls import path
from social.apis import *


urlpatterns = [
    path('recommend',recommend),
    path('like', like),
    path('dislike', dislike),
    path('superlike', superlike),
    path('rewind', rewind),
    path('like_me', like_me),

]