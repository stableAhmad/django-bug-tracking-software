from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
# from WSGIREF.UTIL import FileWrapper
import mimetypes
from datetime import datetime
from .models import report
from django.contrib.auth.models import User
from .models import report , comment
from project.models import project
import os
from django.http import JsonResponse
import json
import json
from types import SimpleNamespace
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os


@login_required(login_url = "signin")
def render_reports(request, id):
    results = report.objects.all().filter(belongs_to__id=id).exclude(state="Closed")
    current_project = project.objects.all().filter(id=id)[0]
    current_project.bugs_count = results.count()
    current_project.save()
    users = User.objects.all()
    usernames = []
    for user in users:
        usernames.append(user.username)
    context = {"project": current_project, "reports": results , "users":usernames}

    if request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get("data") == "reports":
        id = request.headers.get("reportid")
        target_report = results.filter(id=id)[0]
        json_target_report = target_report.to_json()

        comment_section = comment.objects.all().filter(report__id = id).order_by("date")   
        comment_json =  comments_to_json(comment_section)
        report_json = json.dumps(json_target_report)
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
    if request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get("data")=="deletecomment":
        user = request.user.get_username()
        comment_id = request.headers.get("commentid")
        target_comment = comment.objects.all().filter(id= comment_id)[0]
        if(target_comment.commented_by.username == user):
            target_comment.delete()
            id = request.headers.get("reportid")
            return JsonResponse( comments_to_json(comment.objects.all().filter(report__id = id).order_by("date")) , safe = False)

        else:
            return JsonResponse("" , safe = False)  

    if request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get("data")=="newreport":
        json_report = request.headers.get("newreport")
        new_report = json.loads(json_report, object_hook=lambda d: SimpleNamespace(**d))
        new_report.assignedto =  json.loads(new_report.assignedto )
        new_object=  report()
        new_object.title = new_report.title
        new_object.description = new_report.description
        new_object.severity = new_report.impact
        new_object.state = "Open"
        new_object.reported_by = request.user  
       
       
        new_object.date_added = datetime.now()
        new_object.belongs_to = project.objects.all().filter(id = id)[0]
        new_object.attachment = new_report.attachment 
        new_object.save()
        query = Q(username=new_report.assignedto[0])
        for t in new_report.assignedto[1:]:
            query |= Q(username=t)
        final_res = User.objects.all().filter(query)
        new_object.assigned_to.set(final_res)
        return reports_collection_to_json(report.objects.all().filter(belongs_to__id = id))
    if request.method == 'POST' and request.headers.get("ajax") == "true" and request.headers.get("type")=="uploadingfile" and request.headers.get("valid_file")=="valid":
        target_report = report.objects.all().latest("id")

        file = request.FILES.get("file") 
        fss = FileSystemStorage()
        filename = fss.save(file.name , file)
        url = fss.url('static/uploads/'+filename)
        handle_uploaded_file(file)
        
        target_report.attachment = file 
        target_report.save()

    if request.method == 'GET' and request.headers.get("ajax") == "true" and request.headers.get("data")=="closeauthorization":
        cond = "false"
        if request.user in report.objects.all().filter(id = request.headers.get("reportid"))[0].assigned_to.all():
            report.objects.all().filter(id = request.headers.get("reportid")).update(state = "Closed")
            return reports_collection_to_json(report.objects.all().filter(belongs_to__id = id).exclude( state= "Closed") )
        else:
            return JsonResponse(cond, safe = False)    

        
            
        
    return render(request, "project.html", context)

#render after adding and delering

def handle_uploaded_file(f):  
    with open('static/uploads/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

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
