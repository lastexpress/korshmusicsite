from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from shop.models import Category, Product


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
	first_name = models.CharField(max_length=255, verbose_name='Имя')
	last_name = models.CharField(max_length=255, verbose_name='Фамилия')
	email = models.EmailField(verbose_name='Email')
	address = models.CharField(max_length=255, verbose_name='Адрес')
	postal_code = models.CharField(max_length=255, verbose_name='Код города')
	city = models.CharField(max_length=255, verbose_name='Город')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Созданный заказ')
	update = models.DateTimeField(auto_now=True, verbose_name='Обновленный заказ')
	paid = models.BooleanField(default=False)

	def __str__(self):
		return f"Заказ {self.id} | {self.first_name}"

	class Meta:
		ordering = ('-created',)
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Продукт')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return f"{self.order.first_name} | {self.id}"

	def get_cost(self):
		return self.price * self.quantity


