

from django.urls import path
from parents.views import AssociatedChildernView, ParentProfileView


urlpatterns = [

    path('', ParentProfileView.as_view(), name='childern-list'),
    path('my-childern/', AssociatedChildernView.as_view(), name='childern-list'),
]

