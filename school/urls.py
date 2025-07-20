from django.urls import path
from school.views import ClassRoomApiView, SubjectApiView

urlpatterns = [
    path('classroom/', ClassRoomApiView.as_view(), name='classroom_list'),
    path('subject/', SubjectApiView.as_view(), name='classroom_list'),

]
