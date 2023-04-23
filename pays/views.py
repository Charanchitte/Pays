from html import escape


from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User,Professional,Skill,Post,Agreement,Message
from .forms import UserForm,ProfessionalForm,SkillForm
import datetime
from django.core.mail import send_mail
import random
from django.conf import settings
from itertools import chain
from django.db.models import Q
from django.views.decorators.cache import cache_control
from django.template import loader

from datetime import date




def signin(request):
    try:
        del request.session['post_id']
    except KeyError:
        pass
    if request.method =='POST':
        email=request.POST['email']
        pass1=request.POST['pwd']
        if(User.objects.filter(email=email) and User.objects.filter(password=pass1)):
            myuser=User.objects.get(email=email,password=pass1)
            # request.session['id']=myuser.id
            request.session['post_id']=-1
            if myuser.professional.name=='not':
               if(myuser.secondvisit==False):
                return redirect(select,user_id=myuser.user_id)
               else:
                return redirect(homepage,user_id=str(myuser.user_id))
            else:
                return redirect(homepage,user_id=str(myuser.user_id))
        else:
            messages.error(request,"bad crenentials")
            error='Invalid credentials'
            return render(request,'error_login.html',{'error':error})

    return render(request,'login.html')
def signup(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        pass1=request.POST['password']
        if(len(pass1)<6):
             error = 'The password must contain atleast 6 characters'
             return render(request,'error_signup.html',{'error':error})
        if(User.objects.filter(email=email)):
             error = 'A user with this email already exists'
             return render(request,'error_signup.html',{'error':error})
        if(name==""):
             error = 'Please enter your name'
             return render(request,'error_signup.html',{'error':error})
        else:
         error = 'Please enter your name'
         at_index = email.find('@')+1
         domain = email[at_index:]
         if domain != 'iitk.ac.in':
             error='Please use your iitk email'
             return render(request,'error_signup.html',{'error':error})
         else:
          myuser=User.objects.create()
          myuser.name=name
          myuser.email=email
          myuser.password=pass1

          myuser.save()
            # request.session['email']=email
          return redirect(verify,user_id=myuser.user_id,email=email)

    return render(request,'signup.html')

def homepage(request,user_id):
    if(User.objects.filter(user_id=user_id)):
      myuser=User.objects.get(user_id=user_id)
      if(myuser.is_verified):
         if(request.method=='POST'):
            if(request.POST['search']):
             search=request.POST['search']
            #  request.session['search']=search
             return redirect(search_prof,user_id=myuser.user_id,search=search)
            else :
                search='0'
                return redirect(search_prof,user_id=myuser.user_id,search=search)

         return render(request,'homepage.html',{'myuser': myuser})
      else:
          return redirect(verify,user_id=myuser.user_id,email=myuser.email)
    else:
        error='Please login first in order to view the website'
        return render(request,'error_loginup.html',{'error':error})

def select(request,user_id):
  if(User.objects.filter(user_id=user_id)):
    myuser=User.objects.get(user_id=user_id)
    if(myuser.is_verified==True):
      if(request.method=='POST'):
        select=request.POST.get('professional',False)
        if(select=='Yes'):

               myuser.secondvisit=True
               myuser.save()
               return redirect(new_profile,user_id=myuser.user_id)
        else:
               myuser.secondvisit=True
               myuser.save()
               return redirect(homepage,user_id=myuser.user_id)
      return render(request,'pays_select.html')
    else:
        # request.session['email']=myuser.email
        return redirect(verify,user_id=myuser.user_id,email=myuser.email)
  else:
        error='Please login first in order to view the website'
        return render(request,'error_loginup.html',{'error':error})




def new_profile(request,user_id):
  if(User.objects.filter(user_id=user_id)):
    myuser=User.objects.get(user_id=user_id)
    if(myuser.is_verified):
        skills=Skill.objects.all
        if(request.method=='POST'):
               prof_name=request.POST['prof_name']
               mainskill=request.POST['skill1']
               secskill=request.POST['skill2']
               thirdskill=request.POST['skill3']
               email=request.POST['email']
               restime=int(request.POST['res_time'])
               ufw=request.POST['upforwork']
               image=request.POST.get('image')
               if(prof_name=="" or restime == "" or email==""):
                   error='Please enter valid details'
                   return render(request,'equal_skills.html',{'skills':skills,'error':error})
               if(mainskill==secskill or secskill==thirdskill or mainskill==thirdskill):
                   error='Please enter three different skills'
                   return render(request,'equal_skills.html',{'skills':skills,'error':error})
               else:

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
                myuser.professional.prof_img=image
                myuser.professional.save()
                myuser.professional=myuser.professional

                myuser.save()
                return redirect(homepage,user_id=myuser.user_id)
        return render(request,"profile_new.html",{'skills':skills})
    else:
         return redirect(verify,user_id=myuser.user_id,email=myuser.email)

  else:
        error='Please login first in order to view the website'
        return render(request,'error_loginup.html',{'error':error})

def profile(request,user_id):
    if(User.objects.filter(user_id=user_id)):
        myuser=User.objects.get(user_id=user_id)
        if(myuser.is_verified==True):
            if(myuser.professional.name=='not'):
                return render(request,'profile_user.html',{'myuser':myuser})
            else:

                # all_ratings=Rating.objects.all
                # total_rating=0
                # total=0
                # for item in all_ratings:
                #     agrr=Agreement.objects.get(id=item.id)
                #     if agrr.prof_name==myuser.professional.name:
                #         total_rating=total_rating+item.total
                #         total=total+1
                #     if total==0 and total_rating==0:
                #         myuser.professional.rating=0
                #         myuser.professional.no_works=0
                #     else:
                #         myuser.professional.rating=int(total_rating/total)
                #         myuser.professional.no_works=total
                return render(request,'pays_professional.html',{'myuser':myuser})
        else:
            # request.session['email']=myuser.email
            return redirect(verify,user_id=myuser.user_id,email=myuser.email)
    else:
        error='Please login first in order to view the website'
        return render(request,'error_loginup.html',{'error':error})

def update_profile(request,user_id):
   if(User.objects.filter(user_id=user_id)):
    myuser=User.objects.get(user_id=user_id)
    skills=Skill.objects.all
    if(request.method=='POST'):
               prof_name=request.POST['prof_name']
               mainskill=request.POST['skill1']
               secskill=request.POST['skill2']
               thirdskill=request.POST['skill3']
               email=request.POST['email']
               restime=int(request.POST['res_time'])
               ufw=request.POST['upforwork']
               myuser=User.objects.get(user_id=user_id)
               if(mainskill==secskill or secskill==thirdskill or mainskill==thirdskill):
                   return render(request,'equal_skills.html',{'skills':skills})
               else:
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
                return redirect(homepage,user_id=myuser.user_id)
    return render(request,"profile_new2.html",{'skills':skills,'myuser':myuser})
   else:
        error='Please login first in order to view the website'
        return render(request,'error_loginup.html',{'error':error})


def send_otp(email):
    myuser=User.objects.get(email=email)
    subject = 'Your account verification email'
    otp=random.randint(100000,999999)
    message =f'Your otp is  {otp} '
    email_from=settings.EMAIL_HOST
    if(myuser.otp==0):
      send_mail(subject,message,email_from,[email])
      myuser.otp=otp
      myuser.save()

def verify(request,user_id,email):

     myuser=User.objects.get(email=email)

     send_otp(email)
     if request.method=="POST":

        otp=int(request.POST['otp'])
        if(myuser.otp==otp):
                myuser.is_verified=True
                myuser.otp=0
                myuser.save()
                return redirect(signin)
        else:
                messages.error(request,"bad crenentials")
                return render(request,'wrong_otp.html',{'myuser':myuser})
     return render(request,'otp.html',{'myuser':myuser})

def search_prof(request,user_id,search):
    search=str(search)
    myuser2=User.objects.get(user_id=user_id)
    myuser=Professional.objects.all
    a=["not","client"]
    qs = Q(name__icontains=search) | Q(skills__icontains=search) | Q(secskill__icontains=search) | Q(thirdskill__icontains=search)
    qs=Professional.objects.filter(qs).exclude(name="not").order_by('-rating')
    qs=list(qs)
    if(search=='0'):

        qs=Professional.objects.exclude(name="not").order_by('-rating')
    if request.method=="POST":
        ID=request.POST.get('id')
        proffes=Professional.objects.get(id=ID)
        return render(request,'profile_users.html',{'prof':proffes,'myuser':myuser2})

    return render(request,'search.html',{'search':qs,'myuser':myuser2})

def post(request,user_id):
    if(User.objects.filter(user_id=user_id)):
        myuser=User.objects.get(user_id=user_id)
        posts=Post.objects.filter(client=myuser)
        posts2=Post.objects.filter(professional=myuser.professional)
        posts=list(chain(posts,posts2))
        if(myuser.is_verified):
            allprof=Professional.objects.exclude(Q(name='not')|Q(name=myuser.professional.name))
            if(request.method=='POST'):
                if 'prof' in request.POST:
                    proff=request.POST['prof']
                if 'work' in request.POST:
                    work=request.POST['work']
                    pro_name=request.POST['pro_name']
                    deadline=str(request.POST['deadline'])
                    if proff=="" or work =="" or pro_name=="":
                        error='Enter valid details'
                        return render(request,'error_post.html',{'all_prof':allprof,'error':error,'myuser':myuser,'myuser':myuser})
                    currentdate=date.today().strftime('%Y-%m-%d')
                    if(currentdate>deadline):
                        error='Please choose valid date'
                        return render(request,'error_post.html',{'all_prof':allprof,'error':error,'myuser':myuser,'myuser':myuser})
                    new_post=Post.objects.create()
                    new_post.prof_name=proff
                    new_post.client_name=myuser.name
                    new_post.subject=work
                    new_post.Deadline=deadline
                    new_post.client=myuser
                    new_post.pro_name=pro_name
                    new_post.professional=Professional.objects.get(name=proff)

                    new_post.save()
            return render(request,'post.html',{'all_prof':allprof,'myuser':myuser,'posts':posts})
        else:
            return redirect(verify,user_id=myuser.user_id,email=myuser.email)
    else:
        error='Please login first in order to view the website'
        return render(request,'error_loginup.html',{'error':error})
def inbox(request,user_id):
    if(User.objects.filter(user_id=user_id)):
        myuser=User.objects.get(user_id=user_id)
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
                    post.is_selected=True
                    post.save()
                    request.session['post_id']=post_id
                    return redirect(agreement,user_id=myuser.user_id)

                else:
                    post.accept=False
                    post.is_selected=True
                    post.save()
                    return redirect(inbox,user_id=myuser.user_id)
            return render(request,'inbox.html',{'all_prof':all_prof,'myuser':myuser,'posts':posts})
        else:
                return redirect(verify,user_id=myuser.user_id,email=myuser.email)

    else:
        error='Please login first in order to view the website'
        return render(request,'error_loginup.html',{'error':error})

def agreement(request,user_id):
    if(User.objects.filter(user_id=user_id)):
        myuser=User.objects.get(user_id=user_id)
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
                    request.session['post_id']=-1
                    return redirect(inbox,user_id=myuser.user_id)
                  return render(request,'ag_form.html',{'post':pose,'agreements':agreements,'myuser':myuser})
            else:

                agreem=Agreement.objects.filter(client_name=myuser.name)
                agreement2=Agreement.objects.filter(prof_name=myuser.professional.name)
                agreements=list(chain(agreem,agreement2))
                if(request.method=='POST'):

                      work_not=request.POST.get('work_not')
                      rating=(request.POST.get('rating'))
                      if(work_not):
                       w_agree=Agreement.objects.get(id=work_not)
                       proffesi=Professional.objects.get(name=w_agree.prof_name)
                       proffesi.Last_delivary=date.today()
                       proffesi.save()
                       w_agree.work_not=False
                       w_agree.save()
                       return redirect(agreement,user_id=myuser.user_id)
                      if(rating):
                         rating=int(rating)
                         prof_name=request.POST.get('prof_name')
                         agreemen=Agreement.objects.get(id=prof_name)
                         agreemen.rating_done=True
                         agreemen.rating_agree=rating
                         proff=Professional.objects.get(name=agreemen.prof_name)
                         rating=(proff.rating+rating)
                         proff.no_works=proff.no_works+1
                         proff.rating=rating/(proff.no_works)
                         proff.save()
                         agreemen.save()

                         return redirect(agreement,user_id=myuser.user_id)
                return render(request,'ag_form.html',{'agreements':agreements,'myuser':myuser})
        else:
            return redirect(verify,user_id=myuser.user_id,email=myuser.email)
    else:
                error='Please login first in order to view the website'
                return render(request,'error_loginup.html',{'error':error})

def forgot_password(request):
    if request.method=="POST":
        email=request.POST['email']


        return redirect(change_password,email=email)
    return render(request, 'forgot_password.html')

def change_password(request,email):
    myuser= User.objects.get(email=email)

    send_otp(email)
    if request.method=="POST":
        otp=int(request.POST['otp'])
        password=request.POST['pwd']
        if(myuser.otp==otp):
                myuser.is_verified=True
                myuser.password=password
                myuser.otp=0
                myuser.save()
                return redirect(signin)
        else:
                messages.error(request,"bad crenentials")
                return render(request,'wrong_otp2.html',{'myuser':myuser})

    return render(request,'change_password.html',{'myuser':myuser})

def chat_msg(request,user_id):
    if(User.objects.filter(user_id=user_id)):
        myuser=User.objects.get(user_id=user_id)
        if(myuser.is_verified):
            users=User.objects.exclude(user_id=myuser.user_id)
            if request.method=="POST":
                prof=request.POST['prof']
                user1=User.objects.get(user_id=prof)
                return redirect(chat,user_id=myuser.user_id,receiver=user1.user_id)
            return render(request,'user_chat.html',{'users':users,'myuser':myuser})
        else:
            return redirect(verify,user_id=myuser.user_id,email=myuser.email)
    else:
        error='Please login first in order to view the website'
        return render(request,'error_loginup.html',{'error':error})

def chat(request,user_id,receiver):
    if(User.objects.filter(user_id=user_id)):
        myuser=User.objects.get(user_id=user_id)
        if(myuser.is_verified):
            rece=User.objects.get(user_id=receiver)
            msgs=Message.objects.filter(Q(Q(sender_name=myuser.name) & Q(receiver_name=rece.name)) | (Q(sender_name=rece.name) & Q(receiver_name=myuser.name)) ).order_by('date')
            if request.method == "POST":
                msg=request.POST['msg']
                new_msg=Message.objects.create()
                new_msg.sender_name=myuser.name
                new_msg.receiver_name=rece.name
                new_msg.sender=myuser
                new_msg.receiver=rece
                new_msg.message=msg
                new_msg.save()
                return redirect(chat,user_id=myuser.user_id,receiver=rece.user_id)
            return render(request,'chat.html',{'myuser':myuser,'rece':rece,'msgs':msgs})
        else:
            return redirect(verify,user_id=myuser.user_id,email=myuser.email)
    else:
        error='Please login first in order to view the website'
        return render(request,'error_loginup.html',{'error':error})

def logout(request):
    return redirect(signin)











