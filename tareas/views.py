from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate  # para autenticar usuario
# errores de integridad de la base de datos
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required # para proteger funciones/rutas
# Create your views here.

# inicio
def home(request):
    return render(request, 'home.html')

# creando usuario/Formulario
def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # si coinciden, usuario registrado
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)  # para autenticar usuario
                # usuario creado y se redirecciona a esta pagina
                return redirect('tasks')
            except IntegrityError:
                # return HttpResponse('Username already exits') # usuario ya existente
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exits'
                })
        # contraseñas no coinciden
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do no match'
        })

# vista de tareas - pendientes
@login_required
def tasks(request):
    # all: traigo todas las tareas de la base de datos
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=True)
    # filter: request.user: traigo solo las tareas del usuario logueado
    return render(request, 'tasks.html', {'tasks': tasks})

# vista de tareas completadas
@login_required
def tasks_completed(request):
    # all: traigo todas las tareas de la base de datos
    tasks = Task.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    # filter: request.user: traigo solo las tareas del usuario logueado
    return render(request, 'tasks.html', {'tasks': tasks})

# crear tarea
@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            # guarda los datos en un nuevo formulario
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)  # para guardar la nueva tarea
            new_task.user = request.user  # guardar el usuario
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Por favor prove datos validos'
            })

#iniciar sesion
def iniciarSesion(request):
    if request.method == "GET":
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:  # compruebo si el usuario es valido
            return render(request, 'login.html', {  # si no es valido retorno la vista mas un error
                'form': AuthenticationForm,
                'error': 'Usuario o Contraseña no encontrados'
            })
        else:
            login(request, user)  # para guardar la sesion/ autenticar usuario
            return redirect('tasks')

# cerrar sesion
def cerrarSesion(request):
    logout(request)
    return redirect('home')


#editar tarea
@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        # obtiene la tarea con id especificado
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # toma la tarea y lo guarda en una formulario
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            # obtengo de nuevo la tarea y lo guardo en un formulario nuevamente
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': "error al actualizar tarea"})

#marcar una tarea como completada
@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
#eliminar tarea    
@login_required    
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')
