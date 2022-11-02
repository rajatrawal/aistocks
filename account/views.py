from django.http import HttpResponse
from django.shortcuts import render
from .tasks import send_mails
# Create your views here.
def create_account(request):
    return HttpResponse('Account Created')
def send_mail(request):
    send_mails.delay()
    return HttpResponse('mail sent')