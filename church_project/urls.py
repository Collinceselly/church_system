"""
URL configuration for church_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    messages.success(request, f'You have successfully been logged out!')
    return redirect('home_page')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls')),
    path('register/', user_views.register, name = 'register'),
    path('member/register/', user_views.member_account, name = 'register_member'),
    path('member/login/', user_views.member_login, name = 'member_login'),
    path('user/login/', user_views.user_login, name = 'user_login'),
    path('logout/', custom_logout, name = 'logout'),
    path('contributions/', include('contributions.urls')),
    path('children/', include('children.urls')),
]
