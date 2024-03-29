from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.UserSignUpAPIView.as_view(), name='sign-up'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
]
