from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
# from WSGIREF.UTIL import FileWrapper
import mimetypes
from .models import report
from project.models import project
import os
from django.http import JsonResponse
import json


def render_reports(request, id):
    results = report.objects.all().filter(belongs_to__id=id)
    current_project = project.objects.all().filter(id=id)[0]
    current_project.bugs_count = results.count()
    current_project.save()
    context = {"project": current_project, "reports": results}

    if request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get("data") == "reports":
        id = request.headers.get("reportid")
        print("test here")
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
    if request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get(
            "ajaxFunction") == "showOpen" and request.headers.get("method") == "open":
        rep = reports.exclude(state="Closed")
        return reports_collection_to_json(rep)
    elif request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get(
            "ajaxFunction") == "showOpen" and request.headers.get("method") == "all":
        return reports_collection_to_json(reports)
    return render(request, "reports.html", context)


def reports_collection_to_json(repports):
    values = [p.to_json() for p in repports]
    json_list = []

    for value in values:
        json_list.append(json.dumps(value))
    json_list = json.dumps(json_list)
    return JsonResponse(json_list, safe=False)


def download_report_attachment(request, project_id, report_id):
    target = report.objects.all().filter(id=report_id)[0]
    filename = target.attachment.name.split('/')[-1]
    response = HttpResponse(target.attachment, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
