from django.shortcuts import render
from django.http import HttpResponse
from .models import user
from team.models import team


def signed_up(request):
    messDic = {"message": "", "signed": False}

    if request.POST.get("try"):
        DIC = request.POST
        if (DIC.get("first_name") != '' and DIC.get("last_name") != '' and DIC.get("pass") != '' and DIC.get(
                "mail") != '' and DIC.get("team_leader_mail") != ''):
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
        
    return render(request, "signup.html", messDic)


def profile(request):
    return render(request, "profile.html")
