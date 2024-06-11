from django.contrib import admin
from django.urls import path
from website.views import publicaciones, registro_denuncia, create_report, success, mapa, registar, login_web, obteniendo
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

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
    path('api/denuncias/', obteniendo, name='obteniendo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
