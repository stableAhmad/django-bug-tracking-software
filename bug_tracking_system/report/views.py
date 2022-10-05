from django.shortcuts import render
from django.http import HttpResponse
from .models import report


def render_reports(request , id):
	results = report.objects.all().filter(belongs_to__id = id)
	context = {"reports":results}
	return render(request , "project.html",context)
