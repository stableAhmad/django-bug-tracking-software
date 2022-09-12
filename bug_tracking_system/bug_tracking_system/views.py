from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
	return render(request,"base.html")







def sign_in(request):
	return render(request, "signin.html")	