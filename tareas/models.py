from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    # Se relaciona con una tabla user proporcionada por django
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #cuando se elimine la tabla usuario se eliminara tambien sus tareas-- eliminacion cascada


    def __str__(self):
        return self.title +' by '+ self.user.username # funcion que devuelve el titulo de la tarea y el usuario que la creo

