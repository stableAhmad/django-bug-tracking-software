from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.shortcuts import render
from .models import project
from datetime import datetime
from report.models import report

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def home(request):
    assigned = report.objects.all().filter(assigned_to = request.user )
    
    projects = project.objects.all();
    if request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get(
            "ajaxFunction") == "sort":

        try:
            method = request.headers.get("method")

            projects = projects.order_by(method)
            response = final_json_response(projects)

            return response
        except Exception as e:
            print(e)
    elif ((request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get(
            "ajaxFunction") == "search")):
        keyword = request.headers.get("searchWord")
        response = projects.filter(name__startswith=keyword)
        return final_json_response(response)

    elif (request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get(
            "ajaxFunction") == "add"):
        name = request.headers.get("data")
        print(name)
        new_project = project()
        new_project.name = name
        new_project.date_added = datetime.now()
        new_project.bugs_count = 0
        new_project.save()

        return final_json_response(projects)
    elif (request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get(
            "ajaxFunction") == "delete"):
        id = request.headers.get("data")
        project.objects.all().filter(id=id).delete()
        return final_json_response(project.objects.all())
    context = {"projects": projects , "assigned":assigned}

    return render(request, "home.html", context)


def final_json_response(data):
    values = [p.to_json() for p in data]
    json_list = []
    for value in values:
        json_list.append(json.dumps(value))
    json_list = json.dumps(json_list)

    return JsonResponse(json_list, safe=False)
