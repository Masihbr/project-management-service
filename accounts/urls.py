from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.UserSignUpAPIView.as_view(), name='sing-up'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
]
