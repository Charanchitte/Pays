from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
import json
import uuid
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator




# Create your models here.

class Professional(models.Model):


    name = models.CharField(max_length=20, help_text='Enter your name')
    email = models.EmailField(max_length=254,unique = True, help_text='Enter your mail id')
    password=models.CharField(max_length=30,default='null',validators=[MinLengthValidator(6)])
    skills=models.CharField(max_length=20)
    secskill=models.CharField(default='null',max_length=20)
    thirdskill=models.CharField(default='null',max_length=20)
    up_for_work=models.CharField(max_length=3,help_text='Are you up for work')
    response_time=models.IntegerField(default=0,validators=[MinValueValidator(0)])
    member_since=models.DateField(auto_now=True)
    Last_delivary=models.CharField(max_length=100,default='0000-00-00')
    expert_in=models.CharField(max_length=30)
    no_works=models.IntegerField(default=0)
    rating=models.IntegerField(default=0,validators=[MaxValueValidator(5), MinValueValidator(1)])
    prof_img=models.ImageField(null=True,blank=True,upload_to="images/")

    def  __str__(self):
        return self.name

def default_prof():
    return Professional.objects.get(id=1)

class User(models.Model):
    # id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id=models.CharField(max_length=40,default=uuid.uuid4)
    name = models.CharField(max_length=20, help_text='Enter your first name')
    email = models.EmailField(max_length=254,unique = True, help_text='Enter your mail id')
    password = models.CharField(max_length=30, help_text='Set the Password',validators=[MinLengthValidator(6)])
    is_verified=models.BooleanField(default=False)
    otp=models.IntegerField(default=0)
    professional=models.ForeignKey(Professional,on_delete=models.SET_DEFAULT,default=default_prof,db_constraint=False)
    secondvisit=models.BooleanField(default=False)

    def  __str__(self):
        return self.name
class Skill(models.Model):
    skill = models.CharField(max_length=256,help_text='Enter your skills')
    def  __str__(self):
        return self.skill

class Post(models.Model):
    prof_name=models.CharField(max_length=30)
    client_name=models.CharField(max_length=30)
    subject=models.CharField(max_length=2000)
    Deadline=models.CharField(max_length=30)
    accept=models.BooleanField(default=False)
    professional=models.ForeignKey(Professional,on_delete=models.SET_NULL,null=True)
    client=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    is_selected=models.BooleanField(default=False)
    pro_name=models.CharField(max_length=30,default="project1")
class Agreement(models.Model):
    prof_name=models.CharField(max_length=30,default='null')
    client_name=models.CharField(max_length=30,default='null')
    Negotiated_amount=models.IntegerField(default=0,validators=[MinValueValidator(0)])
    post = models.ForeignKey(Post,on_delete=models.SET_NULL,null=True)
    work_not=models.BooleanField(default=True)
    rating_done=models.BooleanField(default=False)
    rating_agree=models.IntegerField(default=0,validators=[MaxValueValidator(5), MinValueValidator(1)])

class Message(models.Model):
    sender_name=models.CharField(max_length=30,default='null')
    receiver_name=models.CharField(max_length=30,default='Null')
    date=models.DateTimeField(auto_now=True)
    sender=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='sender')
    receiver=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='receiver')
    message=models.CharField(max_length=200)
