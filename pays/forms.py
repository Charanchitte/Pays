from django import forms
from .models import  User,Professional,Skill
class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','name','password']

class ProfessionalForm(forms.ModelForm):
    class Meta:
        model=Professional
        fields=['name','email','skills'] 

class SkillForm(forms.ModelForm):
    class Meta:
        model=Skill
        fields=['skill']