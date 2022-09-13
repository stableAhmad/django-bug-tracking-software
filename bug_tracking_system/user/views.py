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
            col = user.objects.all()
            unique = True
            for x in col:
                if mail == x.mail:
                    messDic["message"] = "E-mail is already used"

                    unique = False
                    break
            if unique:
                newUser = user(firstname=DIC["first_name"], lastname=DIC["last_name"], mail=DIC["mail"],
                               password=DIC["pass"], teamleadermail=null, bugsreported=0,
                               bugsclosed=0)
                newUser.save()
                messDic["signed"] = True
                messDic["message"] = "You can sign in now"

                leader = DIC["team_leader_mail"]
                
                # start here
                #foundTL = False
                #teamdb = team.objects.all()

                #for it in teamdb:
                    #if leader == it.teamleader:
                        #it.teammembers.append(mail)
                        #foundTL = True

                #if not foundTL:
                    #newTL = team(teamleadermail=DIC["team_leader_mail"])
                    #newTL.teammembers.append(DIC["mail"])
                   #newTL.save()

        # search about mail
        # tasks
        # 1-search if the e-mail exists then not valid sign up cause user already exists
        # 2-if e-mail doesnt exists we will create new user then ..
        # we will search the team db for the team leader
        # if found then we add a new memebr to the team of that leader
        # if not we create new team in team db with that team leader
        # then we add its that user as its first memebr
        else:
            messDic["message"] = "Please sign up with a valid input"
            print("no valid input")

    return render(request, "signup.html", messDic)


def profile(request):
    return render(request, "profile.html")
