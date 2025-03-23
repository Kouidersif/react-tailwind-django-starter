from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.UserCreationAPIView.as_view(), name="register"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('resend-code/', views.ResendCodeView.as_view(), name="resend-code"),
    path('validate-code/', views.ValidateCodeAPIView.as_view(), name="validate-code"),
    path('social-login/', views.SocialLoginView.as_view(), name="social-login"),
]
