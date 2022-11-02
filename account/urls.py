import imp
from django import views
from django.urls import path
from . import views
urlpatterns = [
    path('createAccount',views.create_account,name='create_account'),
    path('sendMail',views.send_mail,name='send_mail'),
]
