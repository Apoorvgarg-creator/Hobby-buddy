from .views import UserCreateAPIView, UserLoginAPIView
from django.urls import path, include

urlpatterns = [
   path('create/', UserCreateAPIView.as_view(), name='user-create'),
   path('login/', UserLoginAPIView.as_view(),name='user-login')
]
