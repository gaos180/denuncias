from typing import Any
from django.db.models.query import QuerySet
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
from .forms import RegistroDeUsuario
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404

def obteniendo(request):
    denuncias = Denuncia.objects.all()
    denuncias_json = []
    for denuncia in denuncias:
        denuncia_data = {
            "titulo": denuncia.titulo,
            "causa": denuncia.get_causa_display(),
            "asunto": denuncia.asunto,
            "imagen": denuncia.imagen.url ,
            #"fecha_suceso": denuncia.fecha_suceso.strftime("%Y-%m-%d"),# Formatea la fecha
            "latitude": denuncia.latitude,
            "longitude": denuncia.longitude,
            "estado": denuncia.estado,
        }
        denuncias_json.append(denuncia_data)
    return JsonResponse(denuncias_json, safe=False)


def mapa(request):
    registro = Denuncia.objects.all()
    usuarios = User.objects.all()
    context = {"denuncias": registro,
            "usuarios": usuarios
            }
    return render(request, 'website/mapa.html', context)


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

categorias = [
        [0, "Lugar de explotación"],
        [1, "Uso y/o contaminación de recursos naturales"],
        [2, "Residuos, emisiones e inmisiones"]
    ]
estados = [
        [0, "En revisión"],
        [1, "En procedimiento"],
        [2, "Finalizada"],
        [3, "Rechazada"],
        [4, "Deshabilitada"]
    ]
def base_admin(request):
    return render(request, 'website/baseadmin.html')

categorias = [
        [0, "Lugar de explotación"],
        [1, "Uso y/o contaminación de recursos naturales"],
        [2, "Residuos, emisiones e inmisiones"]
    ]
estados = [
        [0, "En revisión"],
        [1, "En procedimiento"],
        [2, "Finalizada"],
        [3, "Rechazada"],
        [4, "Deshabilitada"]
    ]
def base_admin_denuncia(request):
    registro = Denuncia.objects.all()
    usuarios = User.objects.all()
    form = RegistroDeDenuncia()
    causa = request.GET.get('causa')
    fecha_suceso = request.GET.get('fecha_suceso')
    hora_suceso = request.GET.get('hora_suceso')
    fecha_envio = request.GET.get('fecha_envio')
    estado = request.GET.get('estado')
    query = request.GET.get('query')


    # Apply filters before pagination
    if causa:
        registro = registro.filter(causa=causa)
    if fecha_suceso:
        registro = registro.filter(fecha_suceso=fecha_suceso)
    if hora_suceso:
        registro = registro.filter(hora_suceso=hora_suceso)
    if fecha_envio:
        registro = registro.filter(fecha_envio__date=fecha_envio)
    if estado:
        registro = registro.filter(estado=estado)
    if query:
        registro = registro.filter(
            Q(titulo__icontains=query) |
            Q(asunto__icontains=query) |
            Q(username_username_icontains=query)
        )

    # Pagination after filtering
    page_ = request.GET.get('page', 1)
    paginator = Paginator(registro, 5)
    try:
        registro = paginator.page(page_)
    except:
        raise Http404

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
            denuncia_id = request.POST.get("id")
            denuncia = get_object_or_404(Denuncia, id=denuncia_id)
            denuncia.delete()

    context = {
        'entity': registro,
        "paginator": paginator,
        'usuarios': usuarios,
        'form': form,
        'estados': estados,
        'categorias': categorias,
    }
    return render(request, 'website/lista.html', context)

def base_admin_usuario(request):
    form = RegistroDeUsuario()
    form_registro = UserRegisterForm()
    usuarios = User.objects.all()
    is_staff = request.GET.get('is_staff')
    query = request.GET.get('query')

    if is_staff:
        if is_staff.lower() == 'true':
            usuarios = usuarios.filter(is_staff=True)
        elif is_staff.lower() == 'false':
            usuarios = usuarios.filter(is_staff=False)

    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    no_puede = False
    if request.method == "POST":
        if "ver" in request.POST:
            print("ver")
        elif "editar" in request.POST:
            print("editar")
            form = RegistroDeUsuario(request.POST)
            if form.is_valid():
                usuario = get_object_or_404(User, id=request.POST.get("id"))
                print(usuario.username)
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
            if usuario == request.user:
                print("Este es el usuario, no puede eliminarse así mismo")
                no_puede = True
            else:
                usuario.delete()
        elif "crear" in request.POST:
            print("entra a crear")
            form_registro = UserRegisterForm(request.POST)
            if form_registro.is_valid():
                form_registro.save()
            else:
                print("Errores del formulario de registro:", form_registro.errors)


    page_2 = request.GET.get('page',1)
    try:    
        paginator = Paginator(usuarios, 2)
        usuarios = paginator.page(page_2)
    except: 
        raise Http404
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
        "paginator":paginator,
        "entity": user_json,
        "form": form,
        "form_registro": form_registro,
        "no_puede": no_puede,
    }
    return render(request, 'website/lista_user.html', context)





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
                if request.user.is_staff:
                    return redirect(reverse('panel_admin'))
                else:
                    return redirect(reverse('mapa'))
    else:
        form = AuthenticationForm()
    return render(request, 'website/login_1.html', {"form": form})


def terminos_y_condiciones(request):
    return render(request, 'website/terminos_y_condiciones.html')
