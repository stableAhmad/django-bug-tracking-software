from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from user.views import signed_up , sign_in , reidrect_logout
from project.views import home
from .views import base

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',home , name="home"),
    path('',sign_in),
    path('signup',signed_up),
    path('base',base),
    path('logout',reidrect_logout),
    
    path('reset_password/', auth_views.PasswordResetView.as_view() , name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),  name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete")
    
]
