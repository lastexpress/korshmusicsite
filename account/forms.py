from django import forms

class LoginForm(forms.Form):
	class Meta:
		username = forms.CharField()
		password = forms.CharField(widget=forms.PasswordInput)