from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TodoList(models.Model):
	# Модель для создание задачь связанный с группой пользователя Django
	STATUSES = (
		('NW', 'Новый'),
		('WR', 'В работе'),
		('TS', 'Тестирование'),
		('FSH', 'Выполнено'),
	)
	PRIORITYES = (
		('NR', 'Нормальный'),
		('UG', 'Срочный'),
		('HG', 'Высокий'),
		('IT', 'Немедленный'),
	)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кем создан')
	title = models.CharField(max_length=200, verbose_name='Титул задачи')
	body = models.TextField(verbose_name='Тела задачи')
	status = models.CharField(max_length=3, choices=STATUSES, default='NW', verbose_name='Статус')
	priority = models.CharField(max_length=2, choices=PRIORITYES, default='NR', verbose_name='Приоритет')
	create_date = models.DateField(auto_now=True)
	death_line = models.DateField(verbose_name='Дедлине')

	def __str__(self):
		return 'Task: %s, Created: %s' % (self.title, self.create_date)