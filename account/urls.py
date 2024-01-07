from django.urls import path,include
from .views import UserRegistrationView,LoginView,UserProfile,passchange,emailview,reset_password_view
urlpatterns = [
    
    path('register/',UserRegistrationView.as_view(),name='Register'),
    path('login/',LoginView.as_view(),name='Login'),
    path('profile/',UserProfile.as_view(),name='Profile'),
    path('password/',passchange.as_view(),name='Password'),
    path('sendEmail/',emailview.as_view(),name='Send_Email'),
    path('reset/<uid>/<token>/',reset_password_view.as_view(),name='Password_Change'),
]
