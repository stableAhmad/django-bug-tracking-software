from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
# from WSGIREF.UTIL import FileWrapper
import mimetypes
from django.contrib.auth.models import User
from .models import report , comment
from project.models import project
import os
from django.http import JsonResponse
import json

from django.contrib.auth.decorators import login_required


@login_required(login_url = "signin")
def render_reports(request, id):
    results = report.objects.all().filter(belongs_to__id=id)
    current_project = project.objects.all().filter(id=id)[0]
    current_project.bugs_count = results.count()
    current_project.save()
    context = {"project": current_project, "reports": results}

    if request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get("data") == "reports":
        id = request.headers.get("reportid")
        target_report = results.filter(id=id)[0]
        json_target_report = target_report.to_json()

        comment_section = comment.objects.all().filter(report__id = id).order_by("date")   
        comment_json =  comments_to_json(comment_section)
        #comment_json = JsonResponse(comment_json , safe = False)
        report_json = json.dumps(json_target_report)
        #report_json = JsonResponse(report_json, safe=False)
        obj = {
        'report':report_json,
        'comments':comment_json
        }
        obj = json.dumps(obj)
        return JsonResponse(obj , safe = False)
    if request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get("function") == "comment":
        
        content =request.headers.get("content")
        new_comment =  comment()
        new_comment.content = content 
        username = request.user.get_username()
        new_comment.commented_by = User.objects.all().filter(username = username)[0]
        relative_report = report.objects.all().filter(id = request.headers.get("reportid"))[0]
        new_comment.report = relative_report
        new_comment.save()
        comment_section = comment.objects.all().filter(report__id = request.headers.get("reportid")).order_by("date")   
        comment_json =  comments_to_json(comment_section)
        return JsonResponse(comment_json , safe= False)

    return render(request, "project.html", context)





def comments_to_json(comments_query_set):
    values = [ c.to_json() for c in comments_query_set ]
    json_list = []
    for value in values:
        json_list.append(json.dumps(value))

    json_list = json.dumps(json_list)
    return json_list    

def get_final_json_response(list_of_objects):
    json_list = []
    for value in list_of_objects:
        json_list.append(json.dumps(value))

    json_list = json.dumps(json_list)

    return JsonResponse(json_list, safe=False)

@login_required(login_url = "signin")
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


def reports_collection_to_json(repports): #used to get json response for any collection of objects
    values = [p.to_json() for p in repports]
    json_list = []

    for value in values:
        json_list.append(json.dumps(value))
    json_list = json.dumps(json_list)
    return JsonResponse(json_list, safe=False)

@login_required(login_url = "signin")
def download_report_attachment(request, project_id, report_id):
    target = report.objects.all().filter(id=report_id)[0]
    filename = target.attachment.name.split('/')[-1]
    response = HttpResponse(target.attachment, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
