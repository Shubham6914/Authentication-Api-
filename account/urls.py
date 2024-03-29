
from django.urls import path,include
from .views import UserRegistration,UserLogin,UserProfileView,UserChangePasswordView,SendResetEmailView,UserResetPasswordView
urlpatterns = [
    path('register/',UserRegistration.as_view(),name='register'),
    path('login/',UserLogin.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',UserChangePasswordView.as_view(),name='changepassword'),
    path('resetpassword/',SendResetEmailView.as_view(),name='resetpassword'),
    path('resetpassword/<uid>/<token>/',UserResetPasswordView.as_view(),name='resetpassword'),
    
]
