"""Task_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from Task_app import views
from knox.views import LogoutView as KnoxloguotView
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/register/',views.RegisterApi.as_view(),name='register'),
    path('api/login/',views.LoginApi.as_view(),name='login'),
    path('api/logout/',views.KnowLogoutView.as_view(),name='logout'),
    path('api/change_password/',views.ChangePasswordApiView.as_view(),name='change_password'),
    path('api/password_reset/',include('django_rest_passwordreset.urls',namespace='password_rest')), # required mail
]
