from django import forms

from blog.models import CommentBlog

class CommentBlogForm(forms.ModelForm):
	class Meta:
		model = CommentBlog
		fields = ('name', 'email', 'subject', 'text')
		widgets = {
			'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'имя'}),
			'email' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'E-mail'}),
			'subject' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Тема комментария'}),
			'text' : forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Текст комментария'})
		}