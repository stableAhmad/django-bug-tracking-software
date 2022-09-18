from django.http import JsonResponse
import json
from django.shortcuts import render
from .models import project
# Create your views here.

def home(request):
	
	projects = project.objects.all();
	if(request.method == 'GET'and request.headers.get("ajax")=="true"):
		method = request.headers.get("method")
		
		projects = projects.order_by(method)
		values =  [ p.to_json() for p in projects ]
		list_of_json = []
		for value in values :
			list_of_json.append(json.dumps(value))
		
		list_of_json = json.dumps(list_of_json)	
		

	
		
		return JsonResponse(list_of_json , safe = False)
	


	
	context = {"projects":projects}

	return render(request , "home.html" , context)

