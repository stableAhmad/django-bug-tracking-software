from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import user
from team.models import team
import re
from django.contrib.auth.decorators import login_required
from .User_forms.Signup_form import Signup_form
from django.contrib import messages
from django.contrib.auth import login , authenticate , logout





def signed_up(request):
    

    form = Signup_form()
    context = {"message": "", "signed": False , "form" : form}

    if request.method == "POST":
        data = Signup_form(request.POST)
        if(data.is_valid()):
            data.save()
           
            return redirect('/')
        else :
            #"<[^>]*>"
            errs = data.errors
            error_list = []
            for key in errs.keys():
                for error in errs[key]:
                    error_list.append(error)

            context["error_list"] =error_list        
            

            
 
    return render(request, "signup.html", context)


def sign_in(request):
    message = {"message": "The username or password you have entered is not correct"}
    if(request.method == 'POST'):
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username = username , password = password)
        if user is not None:
            login(request ,user)
            return redirect('home')
        else:
            return render(request , "signin.html" , message)
            

    return render(request , "signin.html" )
    
#when trying to access home page and you are not logged in
#@login_required(login_url='')

"""
when trying to access the login / signup page and you already logged in
 if request.user.is_authenticated:
    redirect('home')
"""



def is_valid(form_dic):
    
    for key in form_dic:
        if(form_dic.get(key)==""):
            
            return False
    return True



 

# from django.conf import settings
# from django.contrib.auth import REDIRECT_FIELD_NAME
# # Avoid shadowing the login() view below.
# from django.contrib.auth import login as auth_login
# from django.contrib.sites.models import get_current_site, Site
# from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
# from django.template import RequestContext
# from django.views.decorators.cache import never_cache
# from django.views.decorators.csrf import csrf_protect
# from remember_me.forms import AuthenticationRememberMeForm



# def remember_me_login(request, template_name='registration/login.html',
#           redirect_field_name=REDIRECT_FIELD_NAME,
#           authentication_form=AuthenticationRememberMeForm):
          
#     """
#     Based on login view cribbed from
#     https://github.com/django/django/blob/1.2.7/django/contrib/auth/views.py#L25
    
#     Displays the login form with a remember me checkbox and handles the
#     login action.
    
#     The authentication_form parameter has been changed from
#     ``django.contrib.auth.forms.AuthenticationForm`` to
#     ``remember_me.forms.AuthenticationRememberMeForm``.  To change this, pass a
#     different form class as the ``authentication_form`` parameter.
    
#     """
    
#     redirect_to = request.REQUEST.get(redirect_field_name, '')
    
#     if request.method == "POST":
#         form = authentication_form(data=request.POST)
#         if form.is_valid():
#             # Light security check -- make sure redirect_to isn't garbage.
#             if not redirect_to or ' ' in redirect_to:
#                 redirect_to = settings.LOGIN_REDIRECT_URL
                
#             # Heavier security check -- redirects to http://example.com should
#             # not be allowed, but things like /view/?param=http://example.com
#             # should be allowed. This regex checks if there is a '//' *before* a
#             # question mark.
#             elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
#                     redirect_to = settings.LOGIN_REDIRECT_URL
                    
#             if not form.cleaned_data.get('remember_me'):
#                 request.session.set_expiry(0)
                
#             # Okay, security checks complete. Log the user in.
#             auth_login(request, form.get_user())
            
#             if request.session.test_cookie_worked():
#                 request.session.delete_test_cookie()
                
#             return HttpResponseRedirect(redirect_to)
            
#     else:
#         form = authentication_form(request)
        
#     request.session.set_test_cookie()
    
#     current_site = get_current_site(request)
    
#     return render_to_response(template_name, {
#         'form': form,
#         redirect_field_name: redirect_to,
#         'site': current_site,
#         'site_name': current_site.name,
#     }, context_instance=RequestContext(request))    


