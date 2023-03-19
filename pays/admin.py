from django.contrib import admin
from .models import User,Professional,Skill,Post,Agreement

admin.site.register(User)
admin.site.register(Professional)
admin.site.register(Skill)
admin.site.register(Post)
admin.site.register(Agreement)