from django.contrib import admin
from .models import *

admin.site.register((Symbol,Signal,Ticker))
# Register your models here.
