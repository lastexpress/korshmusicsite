from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from orders.models import Order, OrderItem



class profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
	date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
	desc = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to='image_prof/group/', null=True, blank=True, verbose_name='Аватарка')

	def __str__(self):
		return f"{self.user.username}"

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

class MediaType(models.Model):
	"""Носитель(двд, флешка)"""
	name = models.CharField(max_length=255, verbose_name='Название медианосителя', null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Медианоситель'
		verbose_name_plural = 'Медианосители'

class Genre(models.Model):
	"""Жанр"""
	name = models.CharField(max_length=50, verbose_name='Название жанра')
	desc = models.TextField(verbose_name='Описание жанра', null=True, blank=True)
	slug = models.SlugField(unique=True)

	def get_absolute_url(self):
		return reverse('application:genre_detail', args=[self.slug])

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Жанр'
		verbose_name_plural = 'Жанры'

class Member(models.Model):
	"""Музыкант(член в группе)"""
	name = models.CharField(max_length=255, verbose_name='Имя музыканта')
	slug = models.SlugField()
	image = models.ImageField(upload_to='image_member/', null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Музыкант'
		verbose_name_plural = 'Музыканты'

class Artist(models.Model):
	"""Исполнитель(никнейм музыканта или группы)"""
	name = models.CharField(max_length=255, verbose_name='Исполнитель/группа')
	slug = models.SlugField()
	members = models.ManyToManyField(Member, related_name='artist', verbose_name='Участник')
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')
	desc = models.TextField(null=True)
	image = models.ImageField(upload_to='image_prof/', blank=True, null=True)

	def get_absolute_url(self):
		return reverse('application:artist_detail', args=[self.slug])

	def __str__(self):
		return f"{self.name} | {self.genre.name}"

	class Meta:
		verbose_name = 'Исполнитель'
		verbose_name_plural = 'Исполнители'

class Album(models.Model):
	"""Название Альбома у исполнителя"""
	author = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='Исполнитель')
	name = models.CharField(max_length=250, verbose_name='Название альбома')
	slug = models.SlugField()
	song_list = models.TextField(verbose_name='Трек-лист', null=True, blank=True)
	mediatype = models.ForeignKey(MediaType, on_delete=models.CASCADE, verbose_name='НОСИТЕЛЬ(CD-DVD, PLAYER, Флешка)', null=True, blank=True)
	release_date = models.DateTimeField(default=timezone.now, verbose_name='Дата релиза')
	description = models.TextField(verbose_name='Описание альбома')
	image = models.ImageField(upload_to='image_alb/', blank=True, null=True)
	gen = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Жанр')

	def get_absolute_url(self):
		return reverse('application:album_detail', args=[self.slug])

	def __str__(self):
		return f"{self.author.name} | {self.name}"

	class Meta:
		verbose_name = 'Альбом'
		verbose_name_plural = 'Альбомы'


class SingleMusic(models.Model):
	"""Сингл трек"""
	name = models.CharField(max_length=255, verbose_name='Название трека')
	title = models.CharField(max_length=255, verbose_name='Тип альбома')
	slug = models.SlugField(unique=True, null=True)
	author = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='Исполнитель')
	gen = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')
	album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='Альбом', null=True, blank=True)
	created_music = models.DateTimeField(auto_now_add=True)
	image_track = models.ImageField(upload_to='image_track/', verbose_name='Обложка трека')
	music_upload = models.FileField(upload_to='music_load/')

	def get_absolute_url(self):
		return reverse('application:single_track_detail', args=[self.slug])

	def __str__(self):
		return f"{self.name} | {self.author.name}"

	class Meta:
		verbose_name = 'Загрузка трека'
		verbose_name_plural = verbose_name


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
	parrent = models.ForeignKey(SingleMusic, on_delete=models.CASCADE, verbose_name='Трэк', related_name='comments', null=True)
	reply = models.ForeignKey("Comment", related_name="replies", on_delete=models.SET_NULL, blank=True, null=True)
	comment_body = models.TextField(verbose_name='Текст комментария')
	date_added = models.DateTimeField(auto_now_add=True, verbose_name='Время создания комментария')

	def __str__(self):
		return f"{self.comment_body} | {self.user}"

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'


class PostReview(models.Model):
	name = models.CharField(max_length=250, verbose_name='Имя отправителя отзыва')
	email = models.EmailField(verbose_name='Емаил для связи')
	subject = models.CharField(max_length=250, verbose_name='Тема сообщения')
	text = models.TextField(verbose_name='Текст обращения')

	def __str__(self):
		return f"{self.name} | {self.subject}"

	class Meta:
		verbose_name = 'Отзыв на сайте'
		verbose_name_plural = verbose_name

	verbose_name = 'Отзыв о сайте'
	verbose_name_plural = verbose_name


class poh_art(models.Model):
	art = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='Артисты')
	gen = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')



class ChangeContactPage(models.Model):
	main_title = models.CharField(max_length=250, verbose_name='Главный заголовок')
	title = models.CharField(max_length=250, verbose_name='над главным заголовок')
	contact_title = models.CharField(max_length=250, verbose_name='Заголовок блока контактов')
	map_adress = models.CharField(max_length=250, verbose_name='Адресс, где находится офис')
	phone = PhoneNumberField(null=False, blank=False, unique=True)
	email = models.EmailField(verbose_name='Контактный E-mail')
	vk_url = models.CharField(max_length=250, verbose_name='Ссылка на вк')
	facebook_url = models.CharField(max_length=250, verbose_name='Ссылка на фейсбук')
	twitter_url = models.CharField(max_length=250, verbose_name='Ссылка на твиттер')
	inst_url = models.CharField(max_length=250, verbose_name='Ссылка на инстаграмм')
	tik_tok_url = models.CharField(max_length=250, verbose_name='Ссылка на тик ток')

	def __str__(self):
		return f"{self.main_title} | {self.phone} | {self.email}"

	class Meta:
		verbose_name = 'Замена контактной информации'
		verbose_name_plural = verbose_name