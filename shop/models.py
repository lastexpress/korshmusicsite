from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=255, verbose_name='Название категории')
	slug = models.SlugField()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('application:product_list_by_category', args=[self.slug])

	class Meta:
		ordering = ('name',)
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

class Size(models.Model):
	size_int = models.CharField(max_length=255, verbose_name='Размер')

	def __str__(self):
		return self.size_int

	class Meta:
		verbose_name = 'Размер'
		verbose_name_plural = 'Размеры'

class Brand(models.Model):
	name= models.CharField(max_length=255, verbose_name='Бренд')
	slug = models.SlugField()

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Бренд'
		verbose_name_plural = 'Бренды'

class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
	parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=225, db_index=True, verbose_name='Название продукта')
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд', blank=True, null=True)
	slug = models.SlugField(max_length=225, db_index=True)
	image = models.ImageField(upload_to='shop_image_pr', blank=True, verbose_name='Картинка продукта')
	description = models.TextField(blank=True, verbose_name='Описание продукта')
	size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Размер', blank=True, null=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField()
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	upload = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('application:product_detail', args=[self.id, self.slug])

	class Meta:
		ordering = ('name',)
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'
