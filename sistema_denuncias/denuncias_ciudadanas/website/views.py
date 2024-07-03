from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import Post, PostForm, RegistroDenuncia, Usuario
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib.auth.models import Group
from .forms import ReportForm, RegistroDeDenuncia, User
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import Http404


def obteniendo(request):
    denuncias = RegistroDenuncia.objects.all()
    denuncias_json = []
    for denuncia in denuncias:
        denuncia_data = {
            "titulo": denuncia.titulo,
            "causa": denuncia.get_causa_display(),  # Usa get_FOO_display() para campos con opciones
            "asunto": denuncia.asunto,
            #"fecha_suceso": denuncia.fecha_suceso.strftime("%Y-%m-%d"),  # Formatea la fecha
            "latitude": denuncia.latitude,
            "longitude": denuncia.longitude,
            "estado": denuncia.estado,
        }
        denuncias_json.append(denuncia_data)
    return JsonResponse(denuncias_json, safe=False)

def publicaciones(request):
    publicaciones = Post.objects.all()
    form = PostForm()
    editing = False
    id = None
    if request.method == "POST":
        print(request.POST)
        if "eliminar" in request.POST:
            Post.objects.get(id=request.POST.get("id")).delete()
        elif "editar" in request.POST:
            post = Post.objects.get(id=request.POST.get("id"))
            form = PostForm(instance=post)
            editing = True
            id = post.id
        elif "guardar" in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                if request.POST.get("editing") == "True":
                    post = Post.objects.get(id=request.POST.get("id"))
                    post.titulo = form.cleaned_data["titulo"]
                    post.contenido = form.cleaned_data["contenido"]
                    post.save()
                    editing = False
                    form = PostForm()
                else:
                    form.save()
                    form = PostForm()
    return render(
        request,
        "website/publicaciones.html",
        {
            "publicaciones": publicaciones,
            "formulario": form,
            "editing": editing,
            "id": id,
        },
    )

def mapa(request):
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
            denuncia.save()
            #Se da aviso que todo esta bien
            return redirect(reverse('registro_denuncia')+'?ok')
        else:
            #Se notifica error
            return redirect(reverse('registro_denuncia')+'?error')
    return render(request, 'website/registro_denuncia.html', {'registro_denuncia':registro_denuncia})

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
                return render(request, "website/mapa.html")
    else:
        form = AuthenticationForm()
    return render(request, 'website/login_1.html', {"form": form})






def base_admin(request):
    return render(request, 'website/baseadmin.html')




def base_admin_denuncia(request):
    lista = RegistroDenuncia.objects.all()
    page_ = request.GET.get('page',1)
    try:    
        paginator = Paginator(lista, 2)
        lista = paginator.page(page_)
    except: 
        raise Http404
    
    denuncias_json = []
    denuncias = {
        "entity":lista,
        "paginator":paginator
    }
    #for denuncia in lista:
    #    denuncia_data = {
    #        "entity":denuncia,
    #        "id": denuncia.id,
    #        "titulo": denuncia.titulo,
    #        "causa": denuncia.get_causa_display(),  # Usa get_FOO_display() para campos con opciones
    #        "asunto": denuncia.asunto,
    #        "latitude": denuncia.latitude,
    #        "longitude": denuncia.longitude,
    #        "estado": denuncia.get_estado_display(),
    #        "username": denuncia.username,
    #        "image": denuncia.imagen,
    #    }
    #    denuncias_json.append(denuncia_data)
    return render(request, 'website/lista.html', denuncias)


def base_admin_usuario(request):
    lista_user = User.objects.all()
    page_2 = request.GET.get('page',1)
    try:    
        paginator = Paginator(lista_user, 2)
        lista_user = paginator.page(page_2)
    except: 
        raise Http404
    
    denuncias_usurios = {
        "entity":lista_user,
        "paginator":paginator
    }
    user_json = []
    """for user_d in usermember:
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
        user_json.append(user_data)"""
    return render(request, 'website/lista_user.html', denuncias_usurios)
