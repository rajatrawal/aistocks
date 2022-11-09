
import yfinance as yf
import pandas_ta as ta
from yahoo_fin.stock_info import get_quote_table
from celery import shared_task
from .models import Symbol,Signal
from  threading import Thread
import queue
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
import asyncio

def save_signal(symbol,position,close,color):
    symbol.position = position
    signal=Signal.objects.create(symbol=symbol,position=position,price=close,high=close,low=close,status='active',color=color)
    signal.save()


def calculate_pips(open, close,position):
    if str(open).index('.') >= 3:  # JPY pair
        multiplier = 0.01
    else:
        multiplier = 0.0001
    if position == 'buy':
        pips = round((close - open) / multiplier)
    else:
        pips =round(( open - close) / multiplier)
    return int(pips)

def save_current_signal(current_signal,current_signal_position,close,high_or_low,current_signal_closing,all_signal_objects,symbol):
 
    if len(all_signal_objects) < len(Signal.objects.filter(symbol=symbol)):
        current_signal_closing = True
    else:
        current_signal_closing = False
    if current_signal_closing:
        if current_signal.max_profit < 0 :
            current_signal.status = 'failed'
        else:
            current_signal.status = 'successful'
        current_signal_closing = False
    else:                
            current_signal.max_profit = calculate_pips(current_signal.price,high_or_low,current_signal_position) 
            current_signal.current_profit=calculate_pips(current_signal.price,close,current_signal_position)

    current_signal.save()

def create_signal(symbol):
    data = yf.download(symbol.symbol, period='8d',interval = f'{symbol.timeframe}m')
    data['sma_30'] = ta.sma(data['Close'],30)
    data['sma_100'] = ta.sma(data['Close'],100)
    data = data[['sma_30','sma_100','Close','High','Low']]
    print(data)
    
    position = symbol.current_position
    all_signal_objects = Signal.objects.filter(symbol=symbol)
    current_signal_closing = False
    sma_30=data['sma_30'][-1]
    sma_100=data['sma_100'][-1]
    print(sma_30,sma_100)
    high=0
    low=0
    close = round(data['Close'][-1],4)
    high_price = round(data['High'][-1],4)
    low_price = round(data['Low'][-1],4)
    
    if len(all_signal_objects) > 0 :
        current_signal = all_signal_objects.last()
        high =current_signal.high 
        low= current_signal.low
    
    
    if high_price >high:
        high=high_price
 
    elif low_price < low:
        low = low_price
        
    if (sma_30 > sma_100):
        if position=='sell':
            position = 'buy'
            save_signal(symbol,position,close,'green')
        high_or_low = high
    elif (sma_30 < sma_100):
        if position=='buy' :
            position='sell'
            save_signal(symbol,position,close,'red')
        high_or_low = low
    
    if len(all_signal_objects) > 0: 
        current_signal.low = low
        current_signal.high = high
        if position=='buy':
            high_or_low = high
        else:
            high_or_low = low
        save_current_signal(current_signal,position,close,high_or_low,current_signal_closing,all_signal_objects,symbol)
    symbol.current_position = position
    symbol.save()
    
@shared_task(blind=True)
def create_signal_task(*args):
    name = args[0]
    symbol = Symbol.objects.get(symbol=name)
    create_signal(symbol)
    return 'Done'

# @shared_task
# def update_stock(*stockpicker):
#     thread_list =[]
#     que = queue.Queue()
#     data={}
#     for i in stockpicker:
#         thread = Thread(target=lambda q,arg1:q.put({i:get_quote_table(arg1)}),args=(que,i))
#         thread_list.append(thread)
#         thread_list[-1].start()
#     for thread in thread_list:
#         thread.join()
#     while not que.empty():   
#         result = que.get()
#         data.update(result)
#     # send data to group
#     channel_layer = get_channel_layer()
#     loop = asyncio.new_event_loop()

#     asyncio.set_event_loop(loop)
#     data = {'name':'rajat'}
#     async_to_sync(channel_layer.group_send)("stock_track", {
#         'type': 'stock_update',
#         'message': data,
#     })
#     return ''

    


