
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.urls import reverse
from . import utils

# Create your models here.
class Symbol(models.Model):
    choices = (
        ('buy','Buy'),
        ('sell','Sell'),
    )
    symbol_id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=50,unique=True)
    timeframe = models.IntegerField()
    title = models.CharField(max_length=50,default='',)
    current_position = models.CharField(max_length=4,choices=choices,default='buy')
    def __str__(self) -> str:
        return self.symbol + ' ' + str(self.timeframe)

class Signal(models.Model):
    position_choices = (
        ('buy','Buy'),
        ('sell','Sell'),
    )
    status_choices=(
        ('active','Active'),
        ('failed','Failed'),
        ('successful','Successful'),
    )
    id = models.AutoField(primary_key=True)
    symbol = models.ForeignKey(Symbol,on_delete=models.CASCADE)
    position = models.CharField(max_length=4,choices=position_choices)
    price = models.FloatField()
    high = models.FloatField(default=0)
    low = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    current_profit = models.FloatField(default=0)
    max_profit = models.FloatField(default=0)
    status = models.CharField(choices=status_choices,max_length=10,default='active')
    color = models.CharField(choices=(('green','green'),('red','red')),max_length=10,default='green')
    
    
class Ticker(models.Model):
    name = models.CharField(max_length=500)
    symbol = models.CharField(max_length=500)
    exchange = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('get_stock',args=[self.symbol,])
    

@receiver(pre_save,sender=Symbol)
def symbol_handler(sender,instance,**kwargs):
    if len(Symbol.objects.filter(symbol=instance.symbol)) ==0:
        utils.create_signal_scheduler(instance)



