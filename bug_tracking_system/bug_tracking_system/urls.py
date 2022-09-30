from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path , include
from user.views import signed_up , sign_in , \
 reidrect_logout ,password_reset_view, password_reset_done_view, \
  password_reset_confirm_view , password_reset_complete_view 
from project.views import home
from .views import base

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',home , name="home"),
    path('',sign_in),
    path('signup',signed_up),
    path('base',base),
    path('logout',reidrect_logout),
    path('password_reset',password_reset_view, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
]
