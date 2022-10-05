from django.shortcuts import render
from django.http import HttpResponse
from .models import report
from project.models import project


def render_reports(request , id):
	results = report.objects.all().filter(belongs_to__id = id)
	current_project = project.objects.all().filter(id = id)[0]
	context = {"project":current_project , "reports":results}
	return render(request , "project.html",context)
