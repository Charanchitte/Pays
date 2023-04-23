from django.urls import path
from django.contrib import admin

from .import views
urlpatterns=[
    path('',views.signin,name="pays_login"),
    path('signup',views.signup,name="pays_signup"),
    path('homepage/<user_id>/',views.homepage,name="pays_homepage"),
    path('select/<user_id>',views.select,name="select"),
    path('new_profile/<user_id>',views.new_profile,name="new_profile"),
    path('profile/<user_id>',views.profile,name="profile"),
    path('update_profile/<user_id>',views.update_profile,name="update_profile"),
    path('verify/<user_id>/<email>',views.verify,name="verify"),
    path('search_prof/<user_id>/<search>',views.search_prof,name="search"),
    path('post/<user_id>',views.post,name="post"),
    path('inbox/<user_id>',views.inbox,name="inbox"),
    path('agreement/<user_id>',views.agreement,name="agreement"),
    path('logout/<user_id>',views.logout,name="logout"),
    path('forgot_password',views.forgot_password,name="forgot_password"),
    path('change_password/<email>',views.change_password,name="change_password"),
    path('chat_msg/<user_id>',views.chat_msg,name='chat_msg'),
    path('chat/<user_id>/<receiver>',views.chat,name="chat"),
    path('logout',views.logout,name='logout')

]
