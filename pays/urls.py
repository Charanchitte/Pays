from django.urls import path
from django.contrib import admin

from .import views
urlpatterns=[
    path('',views.signin,name="pays_login"),
    path('signup',views.signup,name="pays_signup"),
    path('homepage',views.homepage,name="pays_homepage"),
    path('select',views.select,name="select"),
    path('new_profile',views.new_profile,name="new_profile"),
    path('profile',views.profile,name="profile"),
    path('update_profile',views.update_profile,name="update_profile"),
    path('verify',views.verify,name="verify"),
    path('search_prof',views.search_prof,name="search"),
    path('post',views.post,name="post"),
    path('inbox',views.inbox,name="inbox"),
    path('agreement',views.agreement,name="agreement"),
    path('logout',views.logout,name="logout")
]