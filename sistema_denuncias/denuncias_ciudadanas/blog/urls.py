"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from website.views import publicaciones, registro_denuncia, create_report, success, mapa, registar, login_web
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", login_web, name="login"),
    path("admin/", admin.site.urls),
    path("publicaciones/", publicaciones),
    path('create_report/', create_report),
    path('success/', success),
    path('mapa/', mapa, name="mapa"),
    path('', mapa),
    path('register/', registar, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('ingreso_denuncia/', registro_denuncia, name='registro_denuncia'),
]
