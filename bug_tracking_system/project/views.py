from django.shortcuts import render
from .models import project
# Create your views here.
def home(request):
	
	projects = project.objects.all();
	messDic = {"projects":projects , "test":[]}

	



	return render(request , "home.html" , messDic)