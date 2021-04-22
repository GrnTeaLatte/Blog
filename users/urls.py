from django.contrib.auth import views as auth_views
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'users/login.html'}, name='login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^register/$', views.register, name='register'),
]