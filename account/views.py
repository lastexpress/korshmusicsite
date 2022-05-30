from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

from .forms import LoginForm

def user_login(request):

	if request.method == 'POST':
		form = LoginForm(request.POST)
		
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])

			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponse('Авторизация успешна')
				else:
					return HttpResponse('Авторизация не прошла проверку')
			else:
				return HttpResponse('Неправильный логин')
	
	else:
		form = LoginForm()

	dic_obj = {'form' : form}

	return render(request, 'account/login.html')