from django.shortcuts import render
from django.http import HttpResponse
from .models import report
from project.models import project

from django.http import JsonResponse

import json


def render_reports(request, id):
    results = report.objects.all().filter(belongs_to__id=id)
    current_project = project.objects.all().filter(id=id)[0]
    current_project.bugs_count = results.count()
    context = {"project": current_project, "reports": results}

    if request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get("data") == "reports":
        id = request.headers.get("reportid")
        target_report = results.filter(id=id)[0].to_json()
        report_json = json.dumps(target_report)
        return JsonResponse(report_json, safe=False)

    return render(request, "project.html", context)


def get_final_json_response(list_of_objects):
    json_list = []
    for value in list_of_objects:
        json_list.append(json.dumps(value))

    json_list = json.dumps(json_list)

    return JsonResponse(json_list, safe=False)


def all_reports(request):
    reports = report.objects.all()
    context = {"reports": reports}

    return render(request, "reports.html", context)
