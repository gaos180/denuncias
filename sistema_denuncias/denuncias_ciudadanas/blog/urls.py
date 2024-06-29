from django.contrib import admin
from django.urls import path
from website.views import registro_denuncia, mapa, registar, login_web, obteniendo, administracion
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("login/", login_web, name="login"),
    path("admin/", admin.site.urls),
    path("accounts/profile/", admin.site.urls),
    path('mapa/', mapa, name="mapa"),
    path('', mapa),
    path('register/', registar, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('ingreso_denuncia/', registro_denuncia, name='registro_denuncia'),
    path('api/denuncias/', obteniendo, name='obteniendo'),
    path('administracion/', administracion, name='administracion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
