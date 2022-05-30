from paypal.standard.forms import PayPalPaymentsForm
import uuid
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from itertools import chain
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.generic.list import ListView
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login
from .models import Genre, Artist, Album, SingleMusic, Member, MediaType, Comment, PostReview, ChangeContactPage, profile
from .forms import CommentForm, PostReviewForm, UserRegistrationForm, UserEditForm, ProfileEditForm, LoginForm
from blog.forms import CommentBlogForm
from blog.models import CategoryList, Blog, CommentBlog
from shop.models import Category, Product
from cart.cart import Cart
from cart.forms import CartAddProductForm
from orders.models import Order, OrderItem
from orders.forms import OrderCreateForm


# class register(View):
# 	template_name = 'account/register.html'

# 	def get(self, request):
# 		context = {'form' : UserCreationForm()}

# 		return render(request, self.template_name, context)

# 	def post(self, request):
# 		form = UserCreationForm(request.POST)

# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			user = authenticate(username=username, password=password)
# 			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
# 			return HttpResponseRedirect(request.path)

# 		dic_obj = {'form' : form}

# 		return render(request, self.template_name, dic_obj)

def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			profile.objects.create(user=new_user)
			login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
			return HttpResponseRedirect(request.path)

			dic_obj = {'new_user' : new_user}

			return render(request, 'account/register_done.html', dic_obj)

	else:
		user_form = UserRegistrationForm()

	dic_obj = {'user_form' : user_form}

	return render(request, 'account/register.html', dic_obj)

@login_required
def Profile(request):
	order = Order.objects.filter(user=request.user)

	dic_obj = {'order':order}

	return render(request, 'account/profile.html', dic_obj)

@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated'\
									  'succesfuly')
		else:
			messages.error(request, 'Error updating your profile')

	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)

	

	dic_obj = {'user_form' : user_form,
			   'profile_form' : profile_form}

	return render(request, 'account/edit.html', dic_obj)


# def edit(request):
# 	if request.method == 'POST':
# 		profile_form = ProfileEditForm(data=request.POST, files=request.FILES)

# 		if profile_form.is_valid():
# 			instance = profile_form.save(commit=False)
# 			instance.user = request.user
# 			instance.save()
# 			return HttpResponseRedirect(request.path)

# 	else:
# 		profile_form = ProfileEditForm(data=request.POST, files=request.FILES)

# 	profile_info = profile.objects.all()

# 	dic_obj = {'profile_form' : profile_form,
# 			   'profile_info' : profile_info}

# 	return render(request, 'account/edit.html', dic_obj)

def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])

			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(request.path)

				else:
					return HttpResponse('ВЫКЛЮЧЕН АК')

			else:
				return HttpResponse('Не правильный логин')
	else:
		form = LoginForm()

	return render(request, 'account/login.html', {'form':form})


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#                     return HttpResponseRedirect(request.path)
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})


class Search(ListView):
	"""Поиск на сайте"""
	template_name = 'search/index.html'
	# model = SingleMusic

	paginate_by = 12

	def get_queryset(self):
		query_set = []
		query_set.append(SingleMusic.objects.filter(name__icontains=self.request.GET.get("q")))
		query_set.append(Album.objects.filter(name__icontains=self.request.GET.get("q")))
		# return SingleMusic.objects.filter(name__icontains=self.request.GET.get("q"))

		final_set = list(chain(*query_set))
		return final_set

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context["q"] = f'q={self.request.GET.get("q")}&'
		return context


def product_list(request, category_slug=None):
	cart = Cart(request)
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	productes = Product.objects.filter(available=True)[:3]
	products_one = Product.objects.get(pk=1)
	products_two = Product.objects.get(pk=2)

	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
		productes = products.filter(category=category)


	dic_obj = {'category' : category,
			   'categories' : categories,
			   'products' : products,
			   'productes' : productes,
			   'products_one' : products_one, 'products_two' : products_two,
			   'cart' : cart}

	return render(request, 'shop/product/index.html', dic_obj)

def product_category_detail(request, slug):
	cart = Cart(request)
	category = get_object_or_404(Category, slug=slug)
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	products = products.filter(category=category)

	dic_obj = {'category' : category,
			   'categories' : categories,
			   'products' : products,
			   'cart' : cart}

	return render(request, 'shop/product/category_detail.html', dic_obj)

def product_detail(request, id, slug):
	product = get_object_or_404(Product, id=id, slug=slug, available=True)
	cart = Cart(request)

	related_products = Product.objects.filter(category=product.category).exclude(id=id)

	cart_product_form = CartAddProductForm()

	categories = Category.objects.all()

	dic_obj = {'product' : product,
			   'categories' : categories,
			   'related_products' : related_products,
			   'cart_product_form' : cart_product_form,
			   'cart' : cart}
	

	return render(request, 'shop/product/detail.html', dic_obj)






@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)

	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])

	return redirect('application:cart_detail')

def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)

	return redirect('application:product_list')

def cart_detail(request):
	cart = Cart(request)


	dic_obj = {'cart' : cart}

	return render(request, 'cart/cart.html', dic_obj)


def payment_procces(request):
	order_id = request.session.get('order_id')
	order = get_object_or_404(Order, id=order_id)
	host = request.get_host()
	paypal_dict = {
		'business' : settings.PAYPAL_RECEIVER_EMAIL,
		'amount' : '20.00',
		'item_name' : f"Заказ {order.id}",
		'invoice' : str(order.id),
		'currency' : 'USD',
	}

	form_pay = PayPalPaymentsForm(initial=paypal_dict)

	dic_obj = {'form':form}

	return render(request, 'payment/procces.html', dic_obj)



def order_create(request):
	cart = Cart(request)

	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			form.instance.user = request.user
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order,
										 product=item['product'],
										 price=item['price'],
										 quantity=item['quantity'])
			cart.clear()

			host = request.get_host()
			paypal_dict = {
				'business' : settings.PAYPAL_RECEIVER_EMAIL,
				'amount': '%.2f' % Decimal(order.get_total_cost()).quantize(Decimal('.01')),
				'item_name' : f"Заказ {order.id}",
				'invoice' : str(order.id),
				'currency' : 'USD',
			}
			form_pay = PayPalPaymentsForm(initial=paypal_dict)

			dic_obj = {'order' : order, 'form_pay' : form_pay}
			return render(request, 'orders/order/created.html', dic_obj)

	else:
		form = OrderCreateForm()

	categories = Category.objects.all()


	dic_obj = {'form' : form,
			   'cart' : cart,
			   'categories' : categories}

	return render(request, 'orders/order/create.html', dic_obj)





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

	comments1 = Comment.objects.filter(parrent=track, reply=None)
	comments = track.comments.filter(reply__isnull=True)

	pk = None
	new_comment = None

	if request.method == 'POST':
		comment_form = CommentForm(request.POST)

		if comment_form.is_valid():
			parent_obj = None
			try:
				reply_id = int(request.POST.get('reply_id'))
			except:
				reply_id = None
			if reply_id:
				parent_obj = Comment.objects.get(id=reply_id)

				content = request.POST.get('comment_body')
				if parent_obj:
					Comment(user=request.user, comment_body=content, reply=parent_obj, parrent=track).save()
				else:
					Comment(parrent = track, user = request.user, comment_body = content).save()
				
				return HttpResponseRedirect(request.path)
            	
			content = request.POST.get('comment_body')
			content = Comment(parrent = track, user = request.user, comment_body = content)
			content.save()
			return HttpResponseRedirect(request.path)
	else:
		comment_form = CommentForm()

	# if request.method == 'POST':
	# 	comment_form = CommentForm(request.user, request.POST, request.FILES)

	# 	if comment_form.is_valid():
	# 		parent_obj = None

	# 		try:
	# 			reply_id = int(request.POST.get('reply_id'))
	# 		except:
	# 			reply_id = None

	# 		if reply_id:
	# 			parent_obj = Comment.objects.get(id=reply_id)
	# 			if parent_obj:
	# 				reply_comment = comment_form.save(commit=False)
	# 				reply_comment.reply = parent_obj

	# 		new_comment = comment_form.save(commit=False)
	# 		new_comment.parrent = track
	# 		new_comment.save()
	# 		return HttpResponseRedirect(request.path)
	# else:
	# 	comment_form = CommentForm()


	dic_obj = {'track' : track,
			   'tracks' : tracks,
			   # 'comment_form' : comment_form,
			   'comments' : comments,
			   'comment_form' : comment_form,
			   'comments1' : comments1}

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