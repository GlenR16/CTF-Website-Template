from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404,FileResponse
import re
from .models import User,Team,Challenge,CTF
from django.views.decorators.csrf import requires_csrf_token
import uuid
from django.urls import reverse

#import pickle

if CTF.objects.first() == None:
    print("Initialising CTF Object.")
    new_ctf = CTF()
    new_ctf.save()
else:
    print("CTF Object exists.")

@requires_csrf_token
def index(request):
    if request.method == 'POST':
        request.session.flush()
    return render(request,'index.html')

def signup(request):
    session = session_verification(request)
    if request.method == 'POST' and session == "":
        email = request.POST.get("email", "")
        name = request.POST.get("name", "")
        password = request.POST.get("password", "")
        if (email!='' and name!='' and password!='' and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) and not User.objects.filter(email=email)) and CTF.objects.first().registrations == True:
            new_user = User(email=email,name=name,password=password)
            new_user.save()
            request.session['email'] = new_user.email
            return redirect(dashboard)
        else:
            return render(request,'signup.html',{'error':True,"CTF":CTF.objects.first()})
    else:
        if session!='':
            return redirect(dashboard)
        else:
            return render(request,'signup.html',{"CTF":CTF.objects.first()})

def login(request):
    session = session_verification(request)
    if request.method == 'POST' and session == "":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        try:
            user = User.objects.get(email=email)
            if (user!='' and password==user.password):
                request.session['email'] = user.email
                return redirect(dashboard)
        except:
            pass
        return render(request,'login.html',{'error':True})
    else:
        if session!='':
            return redirect(dashboard)
        else:
            return render(request,'login.html')

def dashboard(request):
    session = session_verification(request)
    msg = request.GET.get("msg","")
    if session!='':
        user = User.objects.get(email=session)
        if user.team != None and user.team.disqualified == True:
            return render(request,'disqualified.html',{'user':user})
        if CTF.objects.first().started == True:
            challenge = Challenge.objects.all()
            try:
                team = Team.objects.get(tid=user.team.tid)
            except:
                team = ""
            if msg=="Right":
                return render(request,"dashboard.html",{'user':user,"team":team,'challenge':challenge,"CTF":CTF.objects.first(),"flag":True})
            elif msg=="Wrong":
                return render(request,"dashboard.html",{'user':user,"team":team,'challenge':challenge,"CTF":CTF.objects.first(),"flag":False})
            else:
                return render(request,"dashboard.html",{'user':user,"team":team,'challenge':challenge,"CTF":CTF.objects.first()})
        else:
            return render(request,"timer.html",{'user':user})
    else:
        return redirect(login)
    
def flag(request):
    session = session_verification(request)
    if session!='' and request.method == 'POST':
        user = User.objects.get(email=session)
        if  CTF.objects.first().ended != True and CTF.objects.first().started == True and user.team != None and user.team.disqualified != True:
            flag = request.POST.get("flag","")
            cid = request.POST.get("cid","")
            try:
                challenge = Challenge.objects.get(cid=cid)
                team = Team.objects.get(tid=user.team.tid)
            except:
                raise Http404
            if flag != "" and int(cid) not in team.get_solved_challenges() and challenge.flag == flag:
                team.score += challenge.points
                team.set_solved_challenge(cid)
                team.save()
                challenge.solved()
                return HttpResponseRedirect('dashboard?msg=Right')
            else:
                return HttpResponseRedirect('dashboard?msg=Wrong')
        else:
            return HttpResponseRedirect('dashboard')
    else:
        raise Http404

def session_verification(request):
    try:
        session = request.session['email']
    except:
        session = ''
    return session


def profile(request):
    session = session_verification(request)
    if session!='':
        user = User.objects.get(email=session)
        if request.method=='POST' and user.team == None:
            tid = request.POST.get("tid", "")
            name = request.POST.get("name", "")
            if name != "":
                new_team = Team(tid=uuid.uuid4().hex[:8],name=name)
                new_team.save()
                user.team = Team.objects.get(tid=new_team.tid)
                user.save()
            elif tid != "":
                try:
                    new_team = Team.objects.get(tid=tid)
                except:
                    return render(request,"profile.html",{'user':user,'error':True})
                if new_team.members_count() < 5:
                    user.team = Team.objects.get(tid=tid)
                    user.save()
            return HttpResponseRedirect('profile')
        else:
            user = User.objects.get(email=session)
            return render(request,"profile.html",{'user':user,'CTF':CTF.objects.first()})
    else:
        return redirect(login)

def downloads(request,filename):
    if "../" in filename or "'" in filename or '"' in filename:
        raise Http404
    try:
        file = open('ctf\\downloads\\'+filename,'rb')
        return FileResponse(file)
    except:
        raise Http404

def statistics(request):
    challenge = Challenge.objects.all()
    team = Team.objects.all().order_by('-score')
    return render(request, "statistics.html",{"challenge":challenge,"team":team})