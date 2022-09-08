from django.shortcuts import render
from django.http import HttpResponse

def signed_up(request):
	if(request.POST.get("try")):
		DIC = request.POST
		if(DIC.get("first_name") != '' and DIC.get("last_name") != '' and DIC.get("pass") != '' and DIC.get("mail")!= ''):
			print("valid")
		else:
			print("not valid")
	
	return render(request, "signup.html")
