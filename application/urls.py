from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from application import views
from django.contrib.auth import views as auth_views


app_name = 'application'

urlpatterns = [
    path('', views.IndexView, name='home'),
    
    path('search/', views.Search.as_view(), name='search'),
    path('music/genre/', views.GenreView, name='genre'),
    path('music/genre/<str:gen>/', views.genre_detail, name='genre_detail'),
    path('music/artist/<str:author>/', views.artist_detail, name='artist_detail'),
    path('music/track/<str:name>/', views.SingleTrackDetail, name='single_track_detail'),
    path('music/album/<str:pk>/', views.album_detail, name='album_detail'),
    path('music/artist/<str:gen>/all_tracks', views.all_tracks, name='all_tracks'),
    path('contact/', views.contact_page, name='contact_page'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:post>/', views.blog_detail, name='blog_detail'),
    path('category/<str:cat>/', views.category_detail, name='category_detail'),
    path('blog/all_post/', views.blog_all_post, name='blog_all_post'),
    # path('register/', views.register.as_view(), name='register'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.Profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_list/<slug:slug>/', views.product_category_detail, name='product_list_by_category'),
    path('product_list/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('create/', views.order_create, name='order_create'),
    path('payment/', views.payment_procces, name='payment_procces'),
]