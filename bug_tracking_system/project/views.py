from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from .models import project
# Create your views here.

def home(request):
	
	projects = project.objects.all();
	if(request.method == 'GET'and request.headers.get("ajax")=="true"):
		method = request.headers.get("method")
		
		projects = projects.order_by(method)
		
		data = make_serializable(projects)
		final = JsonResponse(data , safe=False)
		print(data)
		return "not yet"
	

	
	context = {"projects":projects}

	return render(request , "home.html" , context)

def make_serializable(Qset):
	list = []
	
	for item in Qset:
		obj_list = []
		obj_list.append("1")
		obj_list.append("2")
		obj_list.append("3")
		obj_list.append("4")
		list.append(obj_list)
		
	return list	
