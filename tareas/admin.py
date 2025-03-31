from django.contrib import admin
from .models import Task
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    readonly_fields =("created",) # para que aparezca la fecha de creación
    
admin.site.register(Task,TaskAdmin) # registramos la clase creada

