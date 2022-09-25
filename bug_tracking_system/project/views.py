from django.http import JsonResponse
import json
from django.shortcuts import render
from .models import project
# Create your views here.

def home(request):
	
	projects = project.objects.all();
	
	if(request.method == 'GET'and request.headers.get("ajax")=="true" and request.headers.get("ajaxFunction")=="sort"):

		try:
			method = request.headers.get("method")

			projects = projects.order_by(method)
			return final_json_response(projects)	
		except Exception as e:
			print(e)
	elif ((request.method == 'GET'and request.headers.get("ajax")=="true" and request.headers.get("ajaxFunction")=="search")):	
		keyword = request.headers.get("searchWord")	
		response = projects.filter(name__startswith = keyword)	
		return final_json_response(response)	
		
	
	

	

	context = {"projects":projects}


	return render(request , "home.html" , context)

def final_json_response(data):
		values = [p.to_json() for p in data]
		json_list = []
		for value in  values:
			json_list.append(json.dumps(value))
		json_list = json.dumps(json_list)
		
		return JsonResponse(json_list , safe = False)	

