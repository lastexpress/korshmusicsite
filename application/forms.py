# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Comment, PostReview, profile

# User = get_user_model()

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('comment_body',)
		widgets = {
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


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
# class UserCreationForm(UserCreationForm):
# 	email = forms.EmailField(label=('Email'),
# 		max_length=255,
# 		widget=forms.EmailInput(attrs={'autocomplete':'email'}))

# 	class Meta(UserCreationForm.Meta):
# 		model = User
# 		fields = ('username', 'email')

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('passwords dont')
		return cd['password2']



class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')
		widgets = {
        	'first_name' : forms.TextInput(attrs={'class':'form-control'}),
        	'last_name' : forms.TextInput(attrs={'class':'form-control'}),
        	'email' : forms.TextInput(attrs={'class':'form-control'}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ('date_of_birth', 'desc', 'image')
        widgets = {
        	'date_of_birth' : forms.TextInput(attrs={'class':'form-control'}),
        	'desc' : forms.TextInput(attrs={'class':'form-control'}),
        }
