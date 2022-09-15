from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import user
from team.models import team


def signed_up(request):
    messDic = {"message": "", "signed": False}

    if request.POST.get("sign_me_up"):
        DIC = request.POST
        if (is_valid(DIC)):
            mail = DIC["mail"]
            query = user.objects.filter(mail = DIC["mail"])
            
            if(query):
                    
                    messDic["message"] = "E-mail is already used"
                    
            else :
                    newUser = user(firstname=DIC["first_name"], lastname=DIC["last_name"], mail=DIC["mail"],
                                password=DIC["pass"],  bugsreported=0,
                                bugsclosed=0)
                    newUser.save()
                    messDic["signed"] = True
                    messDic["message"] = "You can sign in now"


                    leader = DIC["team_leader_mail"]
                    q = team.objects.filter(teamleadermail = leader)
                    if(q):
                        newUser.team = q[0]
                        newUser.save()
                

                    else :
                        newTeam = team(teamleadermail = leader)
                        newTeam.save()
                        newUser.team = newTeam
                        newUser.save()
                    response = redirect("/")
                    return response
        else:
            messDic["message"]="Please use some valid data"
    return render(request, "signup.html", messDic)


def sign_in(request):
    message = {"message": "", "signed": False}
    if(request.POST.get("sign_me_in")):
        
        FORM = request.POST
        if(is_valid(FORM)):
            q = user.objects.filter(mail = FORM["mail"])
            if(q):
                if(FORM["pass"] == q[0].password):
                    message["signed"] = True
                    response =redirect('/home')
                    return response
                else:
                    message["signed"] = False
                    message["message"] = "The password you have entered is not correct"

            else :
                message["signed"] = False
                message["message"] = "The E-mail you have entered is not correct"
        else:
            message["message"]="please insert some valid data"

    return render(request , "signin.html",  message )
    



def is_valid(form_dic):
    
    for key in form_dic:
        if(form_dic.get(key)==""):
            
            return False
    return True


