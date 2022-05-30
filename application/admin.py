from django.contrib import admin

from .models import Genre, Artist, Album, MediaType, Member, SingleMusic, Comment, PostReview, ChangeContactPage, profile
from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'created', 'update', 'paid']
	list_filter = ['paid', 'created', 'update']
	inlines = [OrderItemInline,]
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)



@admin.register(profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'date_of_birth', 'desc']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ('name',)
	prepopulated_fields = {'slug' : ('name',)}

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'genre')
	prepopulated_fields = {'slug' : ('name',)}


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'release_date', 'image')
	prepopulated_fields = {'slug' : ('name',)}

admin.site.register(MediaType)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	prepopulated_fields = {'slug' : ('name',)}

@admin.register(SingleMusic)
class SingleMusicAdmin(admin.ModelAdmin):
	list_display = ('name', 'title', 'author', 'created_music')
	prepopulated_fields = {'slug' : ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'parrent')


@admin.register(PostReview)
class PostReviewAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject')

admin.site.register(ChangeContactPage)