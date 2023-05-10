from django.http import HttpResponse
from django.shortcuts import render
import json
from . models import Signal

# importing utils for utility functions
from  . utils  import *

# importing stocker for tomorrow price production  
# from . import stocker

# importing yahoo fin module
from yahoo_fin.stock_info import get_quote_data,get_company_info,get_financials,get_stats,get_quote_table,get_day_most_active,get_day_losers,get_day_gainers,get_undervalued_large_caps , get_currencies 

# for asyncronise task
from threading import Thread
import queue

# Home Page
def index(request):
    return render(request, 'home/index.html',{'index_page':True})

# Ticker Detail Page
def get_ticker(request, symbol_name):
    # featching exchange name 
    exchange_name,name= get_exchange_name(symbol_name)
    symbol_name_ex = set_exchange_extension(symbol_name,exchange_name)
    # seting as it is true index 
    index=True
    # featching   trading view symbol and  exchange name 
    trading_view_symbol_name,trading_view_exchange_name=get_data_for_tradingview(symbol_name,exchange_name)
    
    #setting criteria for symbol_name
    if symbol_name.startswith('^'):
        symbol_name_ex=symbol_name
        index=False
        trading_view_exchange_name,trading_view_symbol_name=exchange_name,name
    
    try :
        # fetching data 
        more_data = get_quote_data(symbol_name_ex)
        # removing spaces in data
        more_data = remove_space(more_data)

        #geting more data
        more_data['currency'] =get_currency_symbol(more_data['currency'])
        more_data['color'] = calculate_color(more_data['regularMarketChangePercent'])
        more_data['52WLcolor'] = calculate_color(more_data['fiftyTwoWeekLowChangePercent'])
        more_data['52WHcolor'] = calculate_color(more_data['fiftyTwoWeekHighChangePercent'])
        
        more_data['symbolNameNs'] = symbol_name_ex
        more_data['symbolName'] = symbol_name
        more_data['tradingViewExchangeName']=trading_view_exchange_name
        more_data['tradingViewSymbolName']=trading_view_symbol_name
        more_data['todayHigh'] =more_data["regularMarketDayRange"].split('-')[1]
        more_data['todayLow'] =more_data["regularMarketDayRange"].split('-')[0]
    except:
        more_data = {}
    
    # for stocks to fetch more data
    if exchange_name not in  ['FX' , 'CCC'] and index:
        try:
            basic_data = get_quote_table(symbol_name_ex, dict_result=True)
            more_data['sharesOutstanding'] = str(round(more_data['sharesOutstanding']/100000, 2)) + ' Lkh.'
            basic_data['52WH'] = basic_data['52 Week Range'].split('-')[1]
            basic_data['52WL'] = basic_data['52 Week Range'].split('-')[0]
           
            basic_data['shares'] = str(round((more_data['marketCap']/more_data['regularMarketPrice'])/1000000, 2)) + ' Lkh.'
            basic_data['Volume'] = str(round(basic_data['Volume']/1000000, 2))+' Lkh.'
            basic_data['shares'] = str(round((more_data['marketCap']/more_data['regularMarketPrice'])/1000000, 2)) + ' Lkh.'
            new_basic_data = remove_space(basic_data)
            new_basic_data['AvgVolume'] = str(round(new_basic_data['AvgVolume']/1000000, 2))+' Lkh.'
        except:
                new_basic_data = {}

        # fetching statistical data
        try:
            stats = get_stats(symbol_name_ex)
            stats.index = stats['Attribute']
            stats = stats.fillna('N/A')
            stats.drop(columns='Attribute', inplace=True)
            stats = stats.to_dict()['Value']
            stats = remove_space(stats)
            stats['beta_value'] = calculate_risk(stats['Beta5YMonthly'])
        except:
            stats={}

        context = {
            'basic_data': new_basic_data,
            'more_data': more_data,
            'summary': stats,
            'index_page':True
        }
        return render(request, 'home/ticker.html', context)
    else:
        return render(request,'home/ticker2.html',{'more_data':more_data,'index_page':True})

# Signal Page 
def get_signals(request):
    signals = list(Signal.objects.all())
    signals = signals[::-1]
    signals = signals[:20]
    data = {
        'signals':signals,
        'signal_page':True
    }
    return render(request,'home/signals.html',data)

# Chart Page
def chart(request,symbol):
    exchange_name,name= get_exchange_name(symbol)
    trading_view_symbol_name,trading_view_exchange_name=get_data_for_tradingview(symbol,exchange_name)
    if symbol.startswith('^'):
        trading_view_exchange_name,trading_view_symbol_name=exchange_name,name
       
    data = {'symbol':trading_view_symbol_name,'exchange':trading_view_exchange_name}
    return render(request,'home/chart.html',data)
    

# Table Page
def get_table(request,type):
    try:
        if type in ['top gainers','top losers']:
            if type == 'top gainers':
                data = get_day_gainers()  
                
            elif type == 'top losers':
                data = get_day_losers()
            
            data = data.drop(columns='PE Ratio (TTM)')
            data['Volume']= data.Volume.apply(lambda x:  str(round(x/100000,2)) + ' Lkh.')
            data['Market Cap']= data['Market Cap'].apply(lambda x:  str(round(x/100000,2)) + ' Lkh.')
            
        elif type == 'undervalued stocks':
            data = get_undervalued_large_caps()
            data = data.drop(columns='52 Week Range')
            
        elif type == 'currencies':
            data = get_currencies()
            data = data.drop(columns=['52 Week Range','Day Chart'])
        
        data.rename(columns={'Price (Intraday)':'Price','% Change':'%','Avg Vol (3 month)':'Avg Vol 3M'},inplace=True)
        
        columns =  data.columns.to_list()

        data['color']= data.Change.apply(lambda x : calculate_color(x))
        
        data = data.T.to_dict()
        
        context = {
            'data':data,
            'columns':columns,
            'name':type
        }
        
    except:
        context={}
    return render(request,'home/table.html',context=context)

# About Us Page
def about_us(request):
    return render(request,'home/about.html',{'about_page':True})


# return predition of tomorrow price
def predict_ajax_tomorrow(request):
    try:
        symbol_name = request.GET['stockName']
        data = stocker.predict.tomorrow(symbol_name)
        data = json.dumps(data)
        return HttpResponse(data)
    except:
        return HttpResponse("false")

# retrun company basic info
def company_ajax_info(request):
    try:
        symbol_name_ex = request.GET['stockName']
        company_info = get_company_info(symbol_name_ex)
        company_info = company_info.to_dict()
        company_info = company_info['Value']
        company_info = json.dumps(company_info)
        return HttpResponse(company_info)
    except:
        return HttpResponse("false")


# return financial data for bar graph
def get_financial_ajax_data(request):
    try:
        # geting symbol name
        symbol_name_ex = request.GET['stockName'] 
        
        # geting financial data
        financials = get_financials(symbol_name_ex, yearly=True, quarterly=True) 
        
        # spliting data
        anually_balance_sheet = financials['yearly_balance_sheet'].reset_index()
        anually_income_statement = financials['yearly_income_statement'].reset_index().dropna()
        anually_cash_flow = financials['yearly_cash_flow'].reset_index()
        quarterly_income_statement = financials['quarterly_income_statement'].reset_index().dropna()
        
        # get column date wise 
        anually_columns = anually_balance_sheet.columns[1:].astype(str)
        quarterly_columns = quarterly_income_statement.columns[1:].astype(str)
        
        # reformat date
        anually_columns = split_year(anually_columns)
        quarterly_columns = split_month(quarterly_columns)
        # feching quterly data
        quarterly_net_profit = quarterly_income_statement[quarterly_income_statement['Breakdown'] == 'netIncome']
        quarterly_revenue = quarterly_income_statement[quarterly_income_statement['Breakdown'] == 'totalRevenue']
        # feching  data for chart
        anually_net_profit = anually_income_statement[anually_income_statement['Breakdown'] == 'netIncome']
        anually_net_assets = anually_balance_sheet[anually_balance_sheet['Breakdown'] == 'totalAssets']
        anually_cash = anually_balance_sheet[anually_balance_sheet['Breakdown'] == 'cash']
        anually_goodwill = anually_balance_sheet[anually_balance_sheet['Breakdown'] == 'goodWill']
        anually_net_liab = anually_balance_sheet[anually_balance_sheet['Breakdown'] == 'totalLiab']
        anually_revenue = anually_income_statement[anually_income_statement['Breakdown'] == 'totalRevenue']
        
        # feching anually data for financial statement
        anually_balance_sheet.columns = ['Breakdown']+anually_columns[::-1]
        anually_cash_flow.columns = ['Breakdown']+anually_columns[::-1]
        anually_income_statement.columns = ['Breakdown']+anually_columns[::-1]
        quarterly_income_statement.columns = ['Breakdown']+quarterly_columns[::-1]
        
        # droping anually nan data for financial statement
        anually_income_statement = anually_income_statement.dropna().to_dict()
        anually_balance_sheet = anually_balance_sheet.dropna().to_dict()
        anually_cash_flow = anually_cash_flow.dropna().to_dict()
        quarterly_income_statement = quarterly_income_statement.dropna().to_dict()

        chart_json_data = {
            'anuallyNetProfit': create_list(anually_net_profit),
            'quarterlyNetProfit': create_list(quarterly_net_profit),
            'anuallyNetAssets': create_list(anually_net_assets),
            'anuallyNetLiab': create_list(anually_net_liab),
            'anuallyRevenue': create_list(anually_revenue),
            'anuallyCash': create_list(anually_cash),
            'anuallyGoodwill': create_list(anually_goodwill),
            'quarterlyRevenue': create_list(quarterly_revenue),
            'anuallyColumns': anually_columns,
            'quarterlyColumns': quarterly_columns,
        }
        financial_data = {'anuallyIncomeStatement': anually_income_statement, 
                         'anuallyBalanceSheet': anually_balance_sheet,
                         'anuallyCashFlow': anually_cash_flow,
                         'quarterlyIncomeStatement': quarterly_income_statement}
        data = json.dumps([chart_json_data, financial_data])
        return HttpResponse(data)
    except:
        return 'false'



# function to get marquee data  through ajax
def get_marquee_tag_ajax_data(request):
    try:
        most_active = get_day_most_active()
        most_active =most_active[['Symbol',  'Price (Intraday)', 'Change', '% Change', 'Volume']]
        most_active.dropna()
        for i in ['Price (Intraday)','Change']:
            most_active[i]=round(most_active[i],2)
            most_active_dict =most_active.T.to_dict()
            marquee_data=[]
            for key,value in most_active_dict.items():
                value['color'] = calculate_color(value['% Change'])
                marquee_data.append(value)
    except:
        marquee_data = []
    marquee_data = json.dumps(marquee_data)
    return HttpResponse(marquee_data)

# ajax function to get todays highlight  data 
def get_index_ajax_data(request):
    index_symbol = {'sensex':'^BSESN','nifty':'^NSEI','bank nifty':'^NSEBANK','nifty it':'^CNXIT','nasdaq':'^NDX','dax':'^GDAXI'}
    try :
        thread_list =[]
        que = queue.Queue()
        index_data={}
        for key,value in index_symbol.items():
            thread = Thread(target=lambda q,arg1:q.put({key:get_index_data_for_thread(arg1)}),args=(que,value))
            thread_list.append(thread)
            thread_list[-1].start()
        for thread in thread_list:
            thread.join()
        while not que.empty():   
            result = que.get()
            index_data.update(result)    
    except:
        index_data = []
    index_data = json.dumps(index_data)
    return HttpResponse(index_data)

# ajax function to get top gainers etc data 
def get_secondary_index_ajax_data(request):
    def get_calculate_color(params):
        for key,value in params.items():
            value['color']= calculate_color(value['Change'])
        return params
    func_list = [get_day_gainers,get_day_losers,get_undervalued_large_caps]
    data_list =[]
    for i in func_list:
        try:    
            data = i()
            data = data[['Symbol','Price (Intraday)','Change','% Change']]
            data = data.dropna().T.to_dict()
            data = get_calculate_color(data)
        except:
            data =[]
        data_list.append(data)    
    try:
        currencies = get_currencies()[['Symbol','Last Price','Change','% Change']].dropna()
        currencies['color']= currencies.Change.apply(lambda x : calculate_color(x))
        currencies.rename(columns={'Last Price':'Price (Intraday)'},inplace=True)
        currencies = currencies.T.to_dict()
    except:
        currencies={}
    day_stocks = {'top gainers':data_list[0],'top losers':data_list[1],'undervalued stocks':data_list[2],'currencies':currencies}
    day_stocks = json.dumps(day_stocks)
    return HttpResponse(day_stocks)