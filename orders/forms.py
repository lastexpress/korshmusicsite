from django.shortcuts import render
from django import forms

from .models import Order

class OrderCreateForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
		widgets = {
			'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите Имя'}),
			'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите Фамилию'}),
			'email' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите email'}),
			'address' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите адрес'}),
			'postal_code' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Код города'}),
			'city' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите город'}),
		}
