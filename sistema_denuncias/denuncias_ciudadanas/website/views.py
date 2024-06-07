from django.shortcuts import render, redirect
from .models import Post, PostForm
from .forms import ReportForm
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib.auth.models import Group

# Create your views here.
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

def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirige a una página de éxito después de guardar
    else:
        form = ReportForm()
    return render(request, 'website/create_report.html', {'form': form})

def success(request):
    return render(request, 'website/success.html')

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
            user.is_staff = True  # Hacer al usuario personal (opcional)
            user.save()

            group = Group.objects.get(name='denunciantes')
            user.groups.add(group)
            
            login(request, user)
            return redirect('mapa')
    else:
        form = UserRegisterForm()
    return render(request, 'website/register.html', {'form': form})