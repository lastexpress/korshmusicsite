from django.contrib import admin
from .models import Genre, Artist, Album, MediaType, Member, SingleMusic, Comment, AnswerComment, PostReview, ChangeContactPage


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
	list_display = ('comment_name', 'parrent')


@admin.register(AnswerComment)
class AnswerCommentAdmin(admin.ModelAdmin):
	list_display = ('comment_name', 'parrent')

@admin.register(PostReview)
class PostReviewAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject')

admin.site.register(ChangeContactPage)