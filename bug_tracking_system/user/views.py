from django.shortcuts import render , redirect
from django.http import HttpResponse

from team.models import team
import re
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .User_forms.Signup_form import Signup_form
from django.contrib import messages
from django.contrib.auth import login , authenticate , logout 
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from .models import system
from django.conf import settings


def password_reset_view(request):
    if(request.method == "POST"):
        reset_form = PasswordResetForm(request.POST)
        if reset_form.is_valid():
            data = reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                system_obj = system.objects.all().filter(system_name="Django_bug_tracker_system")[0]
                print(system_obj)
                from_email  =system_obj.system_mail
                settings.EMAIL_HOST_USER = from_email
                settings.EMAIL_HOST_PASSWORD = system_obj.system_password
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, from_email , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")

        else:
            print("failure")
    return render(request , 'password_reset.html')

def password_reset_done_view(request):
    return render(request , 'password_reset_done.html')    

def password_reset_confirm_view(request):
    return render(request , 'password_reset_confirm.html')

def password_reset_complete_view(request):
    return render(request , 'password_reset_complete.html')


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
    



def reidrect_logout(request):
    logout(request)
    return redirect('/')

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


