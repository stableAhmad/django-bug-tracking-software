from django.shortcuts import render
from django.http import HttpResponse
from .models import report
from project.models import project

from django.http import JsonResponse


import json

def render_reports(request , id):
	results = report.objects.all().filter(belongs_to__id = id)
	current_project = project.objects.all().filter(id = id)[0]
	
	
	
	context = {"project":current_project , "reports":results}


	if(request.method == 'GET'and request.headers.get("ajax")=="true" and request.headers.get("data")=="reports"):
		reports_list = [ s.to_json() for s in results]
		test = get_final_json_response(reports_list)
		return test
	return render(request , "project.html",context)

def get_final_json_response(list_of_objects):
	json_list = []
	for value in  list_of_objects:
		json_list.append(json.dumps(value))

	json_list = json.dumps(json_list)
		
	return JsonResponse(json_list , safe = False)


def all_reports(request):
	
	return render(request , "reports.html"	)	
