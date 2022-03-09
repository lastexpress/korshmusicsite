from django.contrib import admin

from .models import CategoryList, Blog, CommentBlog

@admin.register(CategoryList)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('cat_name', 'slug')
	prepopulated_fields = {'slug' : ('cat_name',)}


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ('category', 'title', 'slug', 'publish', 'status')
	prepopulated_fields = {'slug' : ('title',)}


@admin.register(CommentBlog)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('post', 'name', 'email', 'subject')
