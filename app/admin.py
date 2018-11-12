from django.contrib import admin
from .models import TodoList
# Register your models here.


class TodoListAdmin(admin.ModelAdmin):
	# Поиск по титулу
	search_fields = ('title', )

admin.site.register(TodoList, TodoListAdmin)
