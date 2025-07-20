from django.urls import path

from exam.views import ExamCreateAPIView, ExamDeleteAPIView, ExamUpdateAPIView

urlpatterns = [
    path('create/', ExamCreateAPIView.as_view(), name='exam-create'),
    path('update/', ExamUpdateAPIView.as_view(), name='exam-update'),
    path('delete/<int:exam_id>/', ExamDeleteAPIView.as_view(), name='exam-delete'),

]
