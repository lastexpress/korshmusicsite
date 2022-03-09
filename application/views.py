from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .models import Genre, Artist, Album, SingleMusic, Member, MediaType, Comment, AnswerComment, PostReview, ChangeContactPage
from .forms import CommentForm, PostReviewForm
from blog.forms import CommentBlogForm
from blog.models import CategoryList, Blog, CommentBlog



def IndexView(request):
	genre = Genre.objects.all()

	mus = SingleMusic.objects.all().order_by("?")

	albums = Album.objects.all().order_by("?")[:4]

	artist = Artist.objects.all()[:4]

	form = PostReviewForm()


	dic_obj = {'genre' : genre,
			   'albums' : albums,
			   'artist' : artist,
			   'mus' : mus,
			   'form' : form}

	return render(request, 'index.html', dic_obj)

def thanks_page(request):
	name = request.POST['name']
	email = request.POST['email']
	subject = request.POST['subject']
	text = request.POST['text']
	element = PostReview(name=name, email=email, subject=subject, text=text)
	element.save()

	dic_obj = {'name' : name,
			   'email' : email,
			   'subject' : subject,
			   'text' : text}

	return render(request, 'thanks_page.html', dic_obj)


def GenreView(request):
	genre = Genre.objects.all()

	dic_obj = {'genre' : genre}

	return render(request, 'genre/genre.html', dic_obj)

def genre_detail(request, gen):
	genre = get_object_or_404(Genre, slug=gen)

	albums = Album.objects.filter(gen_id=genre).order_by('release_date')[:5]

	artists = Artist.objects.filter(genre_id=genre)[:5]

	dic_obj = {'genre' : genre,
			   'albums' : albums,
			   'artists' : artists 
			   }

	return render(request, 'genre/genre_detail.html', dic_obj)


def artist_detail(request, author, pk=6):
	artists = get_object_or_404(Artist, slug=author)

	artest = Artist.objects.all().filter(slug=author)

	track = SingleMusic.objects.filter(author_id=artists)[:5]
	track_one = SingleMusic.objects.filter(author_id=artists)[:1]

	albums = Album.objects.filter(author_id=artists)
	
	similar_artist = Artist.objects.order_by("?")



	dic_obj = {'artists' : artists,
			   'artest' : artest,
			   'track' : track, 'track_one' : track_one,
			   'albums' : albums,
			   'similar_artist' : similar_artist}

	return render(request, 'artist/artist_detail.html', dic_obj)


def SingleTrackDetail(request, name):
	track = get_object_or_404(SingleMusic, slug=name)

	tracks = SingleMusic.objects.filter(slug=name)

	new_comment = None

	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.parrent = track
			new_comment.save()
			return HttpResponseRedirect(request.path)	
	else:
		comment_form = CommentForm()


	dic_obj = {'track' : track,
			   'tracks' : tracks,
			   'comment_form' : comment_form}

	return render(request, 'track/track_detail.html', dic_obj)




def album_detail(request, pk):
	album = get_object_or_404(Album, slug=pk)

	tracks = SingleMusic.objects.filter(album_id=album)
	track_random = SingleMusic.objects.filter(album_id=album).order_by("?")

	dic_obj = {'album': album,
			   'tracks' : tracks, 'track_random' : track_random}

	return render(request, 'album/album_detail.html', dic_obj)


def all_tracks(request, gen=None):
	if gen != 'None':
		artist = get_object_or_404(Artist, slug=gen)
		all_tracks = SingleMusic.objects.filter(author_id=artist)
	else:
		all_tracks = SingleMusic.objects.all()

	albums = Album.objects.filter(author_id=artist)

	




	dic_obj = {'artist' : artist,
			   'all_tracks' : all_tracks,
			   'albums' : albums}
	return render(request, 'track/all_tracks.html', dic_obj)



def contact_page(request):
	contact_info = ChangeContactPage.objects.get(pk=1)

	form = PostReviewForm()
	
	dic_obj = {
				'contact_info' : contact_info,
				'form' : form
			}


	return render(request, 'contact.html', dic_obj)


def blog_list(request):
	post = Blog.published.all()

	posts = Blog.published.all()[:5]

	rec_post = Blog.published.all()[:4]

	categories = CategoryList.objects.all()

	dic_obj = {'post' : post, 'posts' : posts,
			   'rec_post' : rec_post,
			   'categories' : categories}

	return render(request, 'blog/blog_list.html', dic_obj)


def blog_all_post(request):
	posts = Blog.published.all()

	recent_post = Blog.published.all()[:4]

	categories = CategoryList.objects.all()

	#paginations
	objects_list = Blog.published.all()
	paginator = Paginator(objects_list, 10)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)


	dic_obj = {'posts' : posts,
			   'recent_post' : recent_post,
			   'categories' : categories}

	return render(request, 'blog/main.html', dic_obj)


def category_detail(request, cat):
	category = get_object_or_404(CategoryList, slug=cat)

	post = Blog.published.filter(category_id=category)

	rec_post = Blog.published.filter(category_id=category)[:4]

	categories = CategoryList.objects.all()

	#PAGINATIONS
	objects_list = Blog.published.filter(category_id=category)
	paginator = Paginator(objects_list, 4)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)



	dic_obj = {'category' : category,
			   'post' : post,
			   'rec_post' : rec_post,
			   'categories' : categories,
			   'page' : page,
			   'posts' : posts,
			   'objects_list' : objects_list}

	return render(request, 'category/main.html', dic_obj)


def blog_detail(request, year, month, day, post):
	post = get_object_or_404(Blog, slug=post,
								   status='published',
								   publish__year=year,
								   publish__month=month,
								   publish__day=day)

	recent_post = Blog.published.all()[:4]

	categories = CategoryList.objects.all()

	new_comment = None

	if request.method == 'POST':
		comment_forms = CommentBlogForm(data=request.POST)
		if comment_forms.is_valid():
			new_comment = comment_forms.save(commit=False)
			new_comment.post = post
			new_comment.save()
			return HttpResponseRedirect(request.path)	
	else:
		comment_forms = CommentBlogForm()

	dic_obj = {'post' : post,
			   'recent_post' : recent_post,
			   'categories' : categories,
			   'comment_forms' : comment_forms}

	return render(request, 'blog/blog_detail.html', dic_obj)