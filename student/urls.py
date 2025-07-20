from django.urls import path
from .views import *
urlpatterns = [
    path('create/', StudentCreateApiView.as_view(), name='student-list'),
    path('<int:id>/', StudentCreateApiView.as_view(), name='student-create'),
    path('<int:id>/', StudentOnlyUpdate.as_view(), name='student-update'),

]
