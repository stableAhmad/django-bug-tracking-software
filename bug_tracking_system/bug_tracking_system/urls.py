from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path , include
from user.views import signed_up , sign_in , redirect_home , testtest , \
 reidrect_logout ,password_reset_view, password_reset_done_view, \
  password_reset_confirm_view , password_reset_complete_view 
from project.views import home
from report.views import render_reports , all_reports , download_report_attachment
from .views import base

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_home ),
    path('signin',sign_in , name="signin"),
    path('home',home , name="home"),
    path('signup',signed_up),
    path('logout',reidrect_logout , name="logout"),
    path('password_reset',password_reset_view, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('home/<int:id>/', render_reports , name="project"),
    path('reports' , all_reports , name="reports"),
    path('home/<int:project_id>/download/<int:report_id>/' , download_report_attachment , name = "download")
    
]
