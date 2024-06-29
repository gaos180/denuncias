from django.shortcuts import render, redirect
from .models import Post, PostForm, RegistroDenuncia
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib.auth.models import Group
from .forms import ReportForm, RegistroDeDenuncia
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import JsonResponse
#from django.contrib.auth.decorators import login_required


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


def mapa(request):
    context = {}
    if request.user.is_superuser:
        context['message'] = 'Welcome, Superuser!'
        return render(request, 'website/testing.html', context)
    else:
        context['message'] = 'Welcome, Regular User!'
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
            denuncia.save()
            #Se da aviso que todo esta bien
            return redirect(reverse('registro_denuncia')+'?ok')
        else:
            #Se notifica error
            return redirect(reverse('registro_denuncia')+'?error')

    return render(request, 'website/registro_denuncia.html', {'registro_denuncia':registro_denuncia})


def administracion(request):
    registro = RegistroDenuncia.objects.all()
    print(registro)  # Imprime las denuncias en la consola del servidor
    return render(request, 'website/testing.html', {'denuncias': registro})



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
                    return redirect(reverse('administracion'))  # Redirige a la URL de administración
                else:
                    return redirect(reverse('mapa'))
    else:
        form = AuthenticationForm()
    return render(request, 'website/login_1.html', {"form": form})



def terminos_y_condiciones(request):
    return render(request, 'website/terminos_y_condiciones.html')
