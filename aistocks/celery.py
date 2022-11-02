from __future__ import absolute_import,unicode_literals
import os
from celery  import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','aistocks.settings')

app = Celery('aistocks')

app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')

app.conf.update(imports=['home.tasks'])
# app.conf.beat_schedule ={
#     # 'send-mail-every-day':{
#     #     'task':'account.tasks.send_mails',
#     #     'schedule':crontab(hour=13,minute=50),
#     #     # 'arga':   
#     # },
#     # 'every-10-seconds':{
#     #     'task':'home.tasks.update_stock',
#     #     'schedule':10,
#     #     'args':(['ITC.NS'],)
#     # }
    
# }


@app.task(blind=True)
def debug_task(self):
    print(f'Request : {self.request!r}')
    