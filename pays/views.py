
from html import escape
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User,Professional,Skill,Post,Agreement
from .forms import UserForm,ProfessionalForm,SkillForm
import datetime
from django.core.mail import send_mail
import random
from django.conf import settings
from itertools import chain
from django.db.models import Q
from django.views.decorators.cache import cache_control

# @cache_control(no_cache=True, must_revalidate=True)   
def signin(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    try:
        del request.session['post_id']
    except KeyError:
        pass
    try:
        del request.session['email']
    except KeyError:
        pass
    if request.method =='POST':
        email=request.POST['email']
        pass1=request.POST['pwd']
        if(User.objects.filter(email=email) and User.objects.filter(password=pass1)):
            myuser=User.objects.get(email=email,password=pass1)
            request.session['id']=myuser.id
            request.session['post_id']=-1;
            if myuser.professional.name=='not':
                return redirect(select)
            else:
                return redirect(homepage)
        else:
            messages.error(request,"bad crenentials")
            return redirect(signup)
    
    return render(request,'pays_login.html') 
def signup(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        pass1=request.POST['password']
        myuser=User.objects.create()
        myuser.name=name
        myuser.email=email
        myuser.password=pass1
        myuser.save()
        request.session['email']=email

        return redirect(verify)
        
    return render(request,'pays_signup.html')

def homepage(request):
    if(User.objects.filter(id=request.session['id'])):
      myuser=User.objects.get(id=request.session['id'])
      if(myuser.is_verified):
         if(request.method=='POST'):
             search=request.POST['search']
             request.session['search']=search
             return redirect(search_prof)
         return render(request,'1.html')
      else:
          return redirect(verify)
    else:
         return redirect(signin)

def select(request):
  if(User.objects.filter(id=request.session['id'])):
    myuser=User.objects.get(id=request.session['id'])
    if(myuser.is_verified==True):
      if(request.method=='POST'):
        select=request.POST.get('professional',False)
        if(select=='Yes'):
            return redirect(new_profile)
        else:
            return redirect(homepage)  
      return render(request,'select.html')
    else:
        request.session['email']=myuser.email
        return redirect(verify) 
                      
                      
   

def new_profile(request):
  if(User.objects.filter(id=request.session['id'])): 
    skills=Skill.objects.all
    if(request.method=='POST'):
               prof_name=request.POST['prof_name']
               mainskill=request.POST['skill1']
               secskill=request.POST['skill2']
               thirdskill=request.POST['skill3']
               email=request.POST['email']
               restime=request.POST['res_time']
               ufw=request.POST['upforwork']
               myuser=User.objects.get(id=request.session['id'])
               myuser.professional=Professional.objects.create()
               myuser.professional.name=prof_name
               myuser.professional.password=myuser.password
               myuser.professional.email=email
               myuser.professional.skills=mainskill
               myuser.professional.secskill=secskill
               myuser.professional.thirdskill=thirdskill
               myuser.professional.response_time=restime
               myuser.professional.member_since=datetime.datetime.now()  
               myuser.professional.up_for_work=ufw
               myuser.professional.save()
               myuser.professional=myuser.professional
               myuser.save()
               return redirect(homepage)
    return render(request,"profile_new.html",{'skills':skills})
  
def profile(request):
    if(User.objects.filter(id=request.session['id'])):
        myuser=User.objects.get(id=request.session['id'])
        if(myuser.is_verified==True):
            return render(request,'profile.html',{'myuser':myuser})
        else:
            request.session['email']=myuser.email
            return verify()

def update_profile(request):
    skills=Skill.objects.all
    if(request.method=='POST'):
               prof_name=request.POST['prof_name']
               mainskill=request.POST['skill1']
               secskill=request.POST['skill2']
               thirdskill=request.POST['skill3']
               email=request.POST['email']
               restime=request.POST['res_time']
               ufw=request.POST['upforwork']
               myuser=User.objects.get(id=request.session['id'])
               
               myuser.professional.name=prof_name
               myuser.professional.password=myuser.password
               myuser.professional.email=email
               myuser.professional.skills=mainskill
               myuser.professional.secskill=secskill
               myuser.professional.thirdskill=thirdskill
               myuser.professional.response_time=restime
               myuser.professional.up_for_work=ufw
               myuser.professional.save()
               myuser.save()
               return redirect(homepage)
    return render(request,"profile_new.html",{'skills':skills})

def send_otp(email):
    subject = 'Your account verification email'
    otp=random.randint(100000,999999)
    message =f'Your otp is  {otp} '
    email_from=settings.EMAIL_HOST
    send_mail(subject,message,email_from,[email])
    myuser=User.objects.get(email=email)
    myuser.otp=otp
    myuser.save()

def verify(request):
     email=request.session['email']
     myuser=User.objects.get(email=email)
     send_otp(email)
     if request.method=="POST":
        otp=int(request.POST['otp'])
        if(myuser.otp==otp):
                myuser.is_verified=True
                myuser.save() 
                return redirect(signin)
        else:
                messages.error(request,"bad crenentials")
                return redirect(signup)
     return render(request,'otp.html',{'myuser':myuser})

def search_prof(request):
    search=request.session['search']
    search=str(search)
    myuser=Professional.objects.all
    qs = Q(name__icontains=search) | Q(skills__icontains=search) | Q(secskill__icontains=search) | Q(thirdskill__icontains=search)
    qs=Professional.objects.filter(qs)
    qs=list(qs)
    # myuser=Professional.objects.filter(skills=search)
    return render(request,'search.html',{'search':qs})

def post(request):
    if(User.objects.filter(id=request.session['id'])):
        myuser=User.objects.get(id=request.session['id'])
        posts=Post.objects.filter(client=myuser)
        posts2=Post.objects.filter(professional=myuser.professional)
        posts=list(chain(posts,posts2))
        if(myuser.is_verified):
            allprof=Professional.objects.all
            if(request.method=='POST'):
                if 'prof' in request.POST:
                    proff=request.POST['prof']
                if 'work' in request.POST:

                    work=request.POST['work']
                    deadline=request.POST['deadline']
                    new_post=Post.objects.create()
                    new_post.prof_name=proff
                    new_post.client_name=myuser.name
                    new_post.subject=work
                    new_post.Deadline=deadline
                    new_post.client=myuser
                    new_post.professional=Professional.objects.get(name=proff)
                    
                    new_post.save()
            return render(request,'post.html',{'all_prof':allprof,'myuser':myuser,'posts':posts})
        else:
            return redirect(signin)
def inbox(request):
    if(User.objects.filter(id=request.session['id'])):
        myuser=User.objects.get(id=request.session['id'])
        if(myuser.is_verified):
            all_prof=Professional.objects.all
            posts=Post.objects.filter(client=myuser)
            posts2=Post.objects.filter(professional=myuser.professional)
            posts=list(chain(posts,posts2))
            if(request.method=='POST'):
                post_id=request.POST['post_id']
                post=Post.objects.get(id=post_id)
                if(request.POST['accept']=='Accept'):
                    post.accept=True
                    post.save()
                    request.session['post_id']=post_id
                    return redirect(agreement)
                
                else:
                    post.accept=False
                    post.save()
                    return redirect(signin)
            return render(request,'inbox.html',{'all_prof':all_prof,'myuser':myuser,'posts':posts})
        
def agreement(request):
    if(User.objects.filter(id=request.session['id'])):
        myuser=User.objects.get(id=request.session['id'])
        if(myuser.is_verified):
            agreem=Agreement.objects.filter(client_name=myuser.name)
            agreement2=Agreement.objects.filter(prof_name=myuser.professional.name)
            agreements=list(chain(agreem,agreement2))
            if(request.session['post_id'] != -1):
               post_id=request.session['post_id']
               pose=Post.objects.get(id=post_id)
               if(pose.professional==myuser.professional):
                  if(request.method=='POST'):
                    
                    amount=request.POST['rs']
                    agree=Agreement.objects.create()
                    agree.prof_name=pose.prof_name
                    agree.client_name=pose.client_name
                    agree.post=pose
                    agree.Negotiated_amount=amount
                    agree.save()
                  return render(request,'ag_form.html',{'post':pose,'agreements':agreements,'myuser':myuser})
            else:
                
                return render(request,'ag_form.html',{'agreements':agreements,'myuser':myuser})
            
        
def logout(request):
    return redirect(signin)
    

                    

                        






