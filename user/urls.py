from django.urls import path

from user.views import *

urlpatterns = [
    path('signup/', userSignupAPIView.as_view(), name='user-signup'),
    path('login/', userLoginAPIView.as_view(), name='user-signup'),

]
