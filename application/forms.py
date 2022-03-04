from django import forms

from .models import Comment, PostReview

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('comment_name', 'comment_body')
		widgets = {
			'comment_name' : forms.TextInput(attrs={'class':'form-control'}),
			'comment_body' : forms.Textarea(attrs={'class':'form-control'}),
		}

class PostReviewForm(forms.ModelForm):
	class Meta:
		model = PostReview
		fields = ('name', 'email', 'subject', 'text')
		widgets = {
			'name' : forms.TextInput(attrs={'class':'form-control'}),
			'email' : forms.TextInput(attrs={'class':'form-control'}),
			'subject' : forms.TextInput(attrs={'class':'form-control'}),
			'text' : forms.Textarea(attrs={'class':'form-control'})
		}