from django.contrib import admin
from django.urls import path
from website.views import registro_denuncia, administracion, mapa, registar, login_web, obteniendo, terminos_y_condiciones, base_admin, base_admin_denuncia, base_admin_usuario
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
    path('terminos-y-condiciones/', terminos_y_condiciones, name='terminos-y-condiciones'),

    path('a', base_admin, name='panel_admin'),
    path('lista/', base_admin_denuncia, name='panel_admin_denuncia'),
    path('lista_user/', base_admin_usuario, name='panel_admin_user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)