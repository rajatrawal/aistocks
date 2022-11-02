from asyncio import FastChildWatcher
import yfinance as yf
import datetime as dt
def main(stock, years=1,yesterday=False):  # function to get data from Yahoo Finance
    end = dt.datetime.today().strftime('%Y-%m-%d')  # today as the end date
    start = (dt.datetime.today() - dt.timedelta(days=365*years)).strftime('%Y-%m-%d')  # 1 year ago as start
    df = yf.download(stock, start, end)
    if yesterday == True:
        df = df.iloc[:-1,:]
    return df, start, end
main('TATACHEM.NS')

# def calculate_pips(open, close,position):
#     if str(open).index('.') >= 3:  # JPY pair
#         multiplier = 0.01
#     else:
#         multiplier = 0.0001
#     if position == 'buy':
#         pips = round((close - open) / multiplier)
#     else:
#         pips =round(( open - close) / multiplier)
#     return int(pips)

# print(calculate_pips(1.6783,1.6788,'buy'))