from django.shortcuts import render, redirect, get_object_or_404
from .models import Denuncia
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib.auth.models import Group
from .forms import RegistroDeDenuncia
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#from django.contrib.auth.decorators import login_required
from .forms import RegistroDeUsuario


def obteniendo(request):
    denuncias = Denuncia.objects.all()
    denuncias_json = []
    for denuncia in denuncias:
        denuncia_data = {
            "titulo": denuncia.titulo,
            "causa": denuncia.get_causa_display(),
            "asunto": denuncia.asunto,
            #"fecha_suceso": denuncia.fecha_suceso.strftime("%Y-%m-%d"),  # Formatea la fecha
            "latitude": denuncia.latitude,
            "longitude": denuncia.longitude,
            "estado": denuncia.estado,
        }
        denuncias_json.append(denuncia_data)

    return JsonResponse(denuncias_json, safe=False)


def mapa(request):
    if request.user.is_superuser:
        return redirect(reverse('panel_admin'))  # Redirige a la URL de administración
    else:
        return render(request, 'website/mapa.html')


def registar(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.set_password(form.cleaned_data['password1'])
            user.is_staff = False
            user.save()

            group = Group.objects.get(name='denunciantes')
            user.groups.add(group)
            return render(request, "website/mapa.html")
        else:
            return render(request, 'website/register.html', {'form': form})  # Include error messages in context
    else:
        form = UserRegisterForm()
        return render(request, 'website/register.html', {'form': form})


def registro_denuncia(request):
    registro_denuncia = RegistroDeDenuncia()

    if request.method == 'POST':
        registro_denuncia = RegistroDeDenuncia(request.POST, request.FILES)
        if registro_denuncia.is_valid():
            denuncia = registro_denuncia.save(commit=False)
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            denuncia.latitude = float(latitude)
            denuncia.longitude = float(longitude)
            user = request.user
            denuncia.username = user 
            #username = user.get_username()
            #print(username)
            denuncia.save()
            #Se da aviso que todo esta bien
            return redirect(reverse('registro_denuncia')+'?ok')
        else:
            #Se notifica error
            return redirect(reverse('registro_denuncia')+'?error')

    return render(request, 'website/registro_denuncia.html', {'registro_denuncia':registro_denuncia})


def administracion(request):
    registro = Denuncia.objects.all()
    usuarios = User.objects.all()
    form = RegistroDeDenuncia()

    if request.method == "POST":
        if "ver" in request.POST:
            print("ver")
        elif "editar" in request.POST:
            print("editar")
            form = RegistroDeDenuncia(request.POST)
            if form.is_valid():
                denuncia = get_object_or_404(Denuncia, id=request.POST.get("id"))
                denuncia.titulo = form.cleaned_data["titulo"]
                denuncia.asunto = form.cleaned_data["asunto"]
                denuncia.causa = form.cleaned_data["causa"]
                denuncia.estado = request.POST.get("Select")
                denuncia.fecha_suceso = form.cleaned_data["fecha_suceso"]
                denuncia.hora_suceso = form.cleaned_data["hora_suceso"]
                denuncia.consentimiento = form.cleaned_data["consentimiento"]
                denuncia.save()
            else:
                print("Errores del formulario:", form.errors)
        elif "eliminar" in request.POST:
            print("eliminar")
            denuncia = get_object_or_404(Denuncia, id=request.POST.get("id"))
            denuncia.delete()

    context = {
        'denuncias': registro,
        'usuarios': usuarios,
        'form': form,
    }

    return render(request, 'website/testing.html', context)




def base_admin(request):
    return render(request, 'website/baseadmin.html')



def base_admin_denuncia(request):
    registro = Denuncia.objects.all()
    usuarios = User.objects.all()
    form = RegistroDeDenuncia()

    if request.method == "POST":
        if "ver" in request.POST:
            print("ver")
        elif "editar" in request.POST:
            print("editar")
            form = RegistroDeDenuncia(request.POST)
            if form.is_valid():
                denuncia = get_object_or_404(Denuncia, id=request.POST.get("id"))
                denuncia.titulo = form.cleaned_data["titulo"]
                denuncia.asunto = form.cleaned_data["asunto"]
                denuncia.causa = form.cleaned_data["causa"]
                denuncia.estado = request.POST.get("Select")
                denuncia.fecha_suceso = form.cleaned_data["fecha_suceso"]
                denuncia.hora_suceso = form.cleaned_data["hora_suceso"]
                denuncia.consentimiento = form.cleaned_data["consentimiento"]
                denuncia.save()
            else:
                print("Errores del formulario:", form.errors)
        elif "eliminar" in request.POST:
            print("eliminar")
            denuncia = get_object_or_404(Denuncia, id=request.POST.get("id"))
            denuncia.delete()

    context = {
        'denuncias': registro,
        'usuarios': usuarios,
        'form': form,
    }
    return render(request, 'website/lista.html', context)

def base_admin_usuario(request):
    usuarios = User.objects.all()
    form = RegistroDeUsuario()

    if request.method == "POST":
        if "ver" in request.POST:
            print("ver")
        elif "editar" in request.POST:
            print("editar")
            form = RegistroDeUsuario(request.POST)
            if form.is_valid():
                usuario = get_object_or_404(User, id=request.POST.get("id"))
                usuario.first_name = form.cleaned_data["first_name"]
                usuario.last_name = form.cleaned_data["last_name"]
                usuario.email = form.cleaned_data["email"]
                usuario.is_staff = request.POST.get("is_staff") == 'on'
                usuario.save()
            else:
                print("Errores del formulario:", form.errors)
        elif "eliminar" in request.POST:
            print("eliminar")
            usuario = get_object_or_404(User, id=request.POST.get("id"))
            usuario.delete()

    user_json = []
    for user_d in usuarios:
        user_data = {
            "id": user_d.id,
            "username": user_d.username,
            "nombre": user_d.first_name,
            "apellido": user_d.last_name,
            "activo": user_d.is_staff,
            "email": user_d.email,
            "union": user_d.date_joined,
            "sesion": user_d.last_login,
        }
        user_json.append(user_data)

    context = {
        "usuarios": usuarios,
        "lista_user": user_json,
        "form": form,
    }
    return render(request, 'website/lista_user.html', context)

"""
def base_admin_usuario(request):
    usermember = User.objects.all()
    user_json = []
    for user_d in usermember:
        user_data = {
            "id": user_d.id,
            "username": user_d.username,
            "nombre": user_d.first_name,
            "apellido": user_d.last_name,
            "activo": user_d.is_staff,
            "email": user_d.email,
            "union": user_d.date_joined,
            "sesion": user_d.last_login,
        }
        user_json.append(user_data)
    return render(request, 'website/lista_user.html', {"lista_user":user_json})
"""


def login_web(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect(reverse('panel_admin'))
                else:
                    return redirect(reverse('mapa'))
    else:
        form = AuthenticationForm()
    return render(request, 'website/login_1.html', {"form": form})



def terminos_y_condiciones(request):
    return render(request, 'website/terminos_y_condiciones.html')
