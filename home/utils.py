import json
from urllib import request
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from yahoo_fin.stock_info import get_quote_data

def create_signal_scheduler(instance):
    print('signal posted')
    symbol_name = instance.symbol
    timeframe = instance.timeframe
    name = f'signalname-{symbol_name}-{timeframe}'
    schedule,created =CrontabSchedule.objects.get_or_create(minute='*/'+str(timeframe))
    PeriodicTask.objects.create(crontab=schedule,name=name,task='home.tasks.create_signal_task',args=json.dumps([symbol_name]))
    print('signal created')
    


def split_year(date):
    year_list = []
    for i in date:
        year_list.append(i.split(' ')[0].split('-')[0])
    return year_list[::-1]


def split_month(date):
    months = ["January", "February", "March", "April", "May",
              "June", "July", "August", "September", "October", "November", "December"]
    month_list = []
    for i in date:
        month_list.append(' '.join(
            [months[int(i.split(' ')[0].split('-')[1])-1], i.split(' ')[0].split('-')[0]]))
    return month_list[::-1]


def create_list(array):
    if array.shape[0] != 0:
        return (array.values[0][1:]/10000000).astype(str).tolist()[::-1]
    else:
        return []


def get_index_data_for_thread(index):
    symbol_data = get_quote_data(index)
    symbol_data['color'] = calculate_color(symbol_data['regularMarketChangePercent'])
    symbol_data = remove_space(symbol_data)
    return symbol_data

def modify_data(stock_list):
    temp_list=[]
    for i in stock_list:
        i['change'] = round(i['ltp']-i['previousPrice'],2)
        i['changePerc'] = round(((i['ltp']-i['previousPrice'])/i['previousPrice'])*100,2)
        i['color'] = calculate_color(i['changePerc'])
        i['tradedQuantity'] =  str(round(i['tradedQuantity']/1000000,2)) 
        temp_list.append(i)
    return temp_list

def set_exchange_extension(symbol_name,exchange_name):
    exchange_dict = {'NSE':'.NS','NYSE':'','CCC':'','NASDAQ':'','FX':''}
    symbol_name_ex = symbol_name+exchange_dict.get(exchange_name,exchange_name)
    return symbol_name_ex

def get_data_for_tradingview(symbol_name,exchange_name):
    trading_view_exchange_name=exchange_name
    trading_view_symbol_name=symbol_name
        
    exchange_dict = {'FOREX':'FX','CCC':'BINANCE','NSE':'BSE','BUE':'BYMA','CCS':'BVCV','DOH':'QSE','EBS':'SIX','GER':'XETR','IOB':'LSIN','IST':'BIST','JKT':'IDX','PNK':'OTC','STU':'SWB','TLV':'TASE','TOR':'TSX','TW':'TPEX','KOE':'KRX','KSC':'KRX','CPH':'OMXCOP'}
    
    if exchange_name=='FX':
        symbol_name_splited=symbol_name.split('=')[0]
        if symbol_name_splited.endswith('USD'):
            trading_view_symbol_name=symbol_name_splited
        else:
            trading_view_symbol_name='USD'+symbol_name_splited
   

    trading_view_exchange_name = exchange_dict.get(trading_view_exchange_name,trading_view_exchange_name)
    

    return trading_view_symbol_name,trading_view_exchange_name



def calculate_color(x):
    return 'green' if x > 0 else 'red'


def calculate_risk(x):
    try:
        x = float(x)
        if x <= 1:
            return {'color': 'green', 'risk': 'Low'}
        elif x >= 1 and x <= 2:
            return {'color': 'yellow', 'risk': 'Medium'}
        else:
            return {'color': 'red', 'risk': 'High'}
    except:
        return False
# Create your views here.


def remove_space(dictionery):
    data = {}
    punc = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':',
            ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ' ']
    for key, value in dictionery.items():
        key = str(key)
        new_key = ''
        for i in key:
            if i not in punc:
                new_key += i
        if type(value) == float:
            value = round(value, 2)
        data[new_key] = value
    return data

def get_exchange_name(symbol_name):
    symbol_name = symbol_name.split('.')[0]

    stocks_data = json.load(open('./static/home/stocks.json','r'))

    exchange_name = ''
    name = ''
    for i in stocks_data:
        if i['symbol'] == symbol_name:
            exchange_name = i['exchange']
            name = i['name']
            break
            
    return exchange_name,name

def get_currency_symbol(name):
    currency_list = json.load(open('home/currency.json','r',encoding='cp850'))
    for i in currency_list:
        if i['code']==name:
            return i['symbol']
        
        