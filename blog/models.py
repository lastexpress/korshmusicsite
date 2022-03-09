from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


#Менеджер для загрузки постов
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')


class CategoryList(models.Model):
	cat_name = models.CharField(max_length=255, verbose_name='Название категории')
	slug = models.SlugField()

	def __str__(self):
		return self.cat_name

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'


class Blog(models.Model):
	STATUS_CHOICES = (
		('close', 'Close'),
		('published', 'Published'),
	)
	category = models.ForeignKey("CategoryList", on_delete=models.CASCADE, verbose_name='Выбор категории')
	type_blog = models.CharField(max_length=255, verbose_name='Тип Поста')
	title = models.CharField(max_length=255, verbose_name='Заголовок поста')
	slug = models.SlugField(unique_for_date='publish')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Владелец поста')
	pre_body = models.TextField(verbose_name='Описание поста на предисловие')
	body = models.TextField(verbose_name='Описание поста полным текстом')
	publish = models.DateTimeField(default=timezone.now)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)
	image_blog = models.ImageField(upload_to='image_blog/', verbose_name='Картинка блога')
	status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='published', verbose_name='Статус')

	published = PublishedManager()

	def get_absolute_url(self):
		return reverse('application:blog_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

	def __str__(self):
		return f"{self.title}"

	class Meta:
		ordering = ('-publish',)


class CommentBlog(models.Model):
	post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=255, verbose_name='Имя комментатора')
	email = models.EmailField()
	subject = models.CharField(max_length=255, verbose_name='Тема комментария')
	text = models.TextField(verbose_name='Текст комментария')
	comment_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.post} | {self.name} | {self.email}"

	class Meta:
		verbose_name = 'Комментарий к блогу'
		verbose_name_plural = verbose_name