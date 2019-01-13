#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: analyzer.py
# version: 0.1.1
# description: analyzer


import futuquant as ft
import pandas as pd
pd.options.mode.chained_assignment = None


from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import futuquant as ft
import pandas as pd
pd.options.mode.chained_assignment = None



from datetime import datetime, timedelta

q = ft.OpenQuoteContext(host='sz.omg.tf', port=11111)

#hs['code'] = hs['code'].map(lambda x: x[3:])
# 富途牛牛Code
# 沪深A股
hs = q.get_plate_stock('SH.3000005')[1]
ftid = hs.set_index('code').drop(columns=['stock_owner','stock_name', 'lot_size', 'stock_child_type', 'stock_type', 'list_time']).T.to_dict('records')[0]



def datechange(date, change):
    d = datetime.strptime(date,'%Y-%m-%d').date()
    new_d = d + timedelta(days=change)
    new_date = new_d.strftime('%Y-%m-%d')
    return new_date


def trading_day(date, change=0):
    if change <= 0:
        c = ((-change // 4) + 1) * 7
        startdate = datechange(date, -c)
        enddate=date
    else:
        c = ((change // 4) + 1) * 7
        startdate = datechange(date, 1)
        enddate = datechange(date, c)
    tradingdatelist = q.get_trading_days('SH', start=startdate, end=enddate)[1]
    if change <= 0:
        tradingdate = tradingdatelist[-1-change]
    else:
        tradingdate = tradingdatelist[change-1]
    return tradingdate



def Qdata(ftcode, date, day=15, future=False):
    change = - (day + 19)
    start_date = trading_day(date, change=change)
    end_date = trading_day(date)
    data = q.get_history_kline(ftcode, start=start_date, end=end_date, ktype=ft.KLType.K_DAY, autype=ft.AuType.QFQ)[1]
    if len(data) != -change:
        # print(1)
        start_date = datechange(date, -300)
        data = q.get_history_kline(ftcode, start=start_date, end=end_date, ktype=ft.KLType.K_DAY, autype=ft.AuType.QFQ)[1][change:]
    data['ma5'] = data['close'].rolling(5).mean()
    data['ma10'] = data['close'].rolling(10).mean()
    data['ma15'] = data['close'].rolling(15).mean()
    data['ma20'] = data['close'].rolling(20).mean()
    data = data[-day:]
    return data



def mod0(data):
    result = False
    d1ma5 = data.iloc[-1]['ma5']
    d1close = data.iloc[-1]['close']
    if d1close < d1ma5:
        result = True
    return result


def mod1(data, before=7, after=1):
    result = True
    for d in range(after-1, before+1):
        i = - (d + 1)
        ma5 = data.iloc[i]['ma5']
        ma10 = data.iloc[i]['ma10']
        ma15 = data.iloc[i]['ma15']
        ma20 = data.iloc[i]['ma20']
        if not ma5 < ma10 < ma20:
            result = False
            break
    return result



def mod2(data):
    d1ma5 = data.iloc[-1]['ma5']
    d2ma5 = data.iloc[-2]['ma5']
    d3ma5 = data.iloc[-3]['ma5']
    if d1ma5 > d3ma5 > d2ma5: 
        result = True
    return result


def mod3(data):
    result = False
    d1ma5 = data.iloc[-1]['ma5']
    d1ma10 = data.iloc[-1]['ma10']
    d1ma15 = data.iloc[-1]['ma15']
    d1ma20 = data.iloc[-1]['ma20']
    if d1ma5 > d1ma10 and d1ma5 > d1ma15 and d1ma5 > d1ma20: 
        result = True
    return result

    
    




def mod4(data):
    d1ma5 = data.iloc[-1]['ma5']
    d2ma5 = data.iloc[-2]['ma5']
    d3ma5 = data.iloc[-3]['ma5']
    d1ma20 = data.iloc[-1]['ma20']
    d2ma15 = data.iloc[-2]['ma15']
    d3ma10 = data.iloc[-3]['ma10']
    if d1ma5 > d1ma20 and d2ma5 > d2ma15 and d3ma5 > d3ma10: 
        result = True
    return result








df = pd.DataFrame(columns=['code', 'date']





class model4ft():
    def __init__(self, date, day=8):
        self.date = trading_day(date)
        self.day = dayz
        self.df = pd.DataFrame(columns=['code', 'date'])
    def model4(self, code, select_date):
        start_date = datechange(select_date, -45)
        data = Qdata(code, select_date)
        d0 = data.iloc[-1]['time_key'].split(' ')[0]
        if mod1(data, self.day) and mod2(data):
            self.df.loc[len(self.df)] = [code, d0]
        else:
            pass
    def analyze_model4(self, code, date):
        #print(code)
        r = self.model4(code, date)
    def analyze(self):
        futures = []
        with ThreadPoolExecutor(max_workers=200) as executor:
            for i in ftid:
                futures.append(executor.submit(self.analyze_model4, i, self.date))
            kwargs = {'total': len(futures)}
            for f in tqdm(as_completed(futures), **kwargs):
                pass
    def result(self):
        print(self.df.to_string)



a = model4ft('2018-12-12')
a.analyze()


                  
                  

class model5ft():
    def __init__(self, date, day=8):
        self.date = trading_day(date)
        self.day = day
        self.df = pd.DataFrame(columns=['code', 'date'])
    def model4(self, code, select_date):
        start_date = datechange(select_date, -45)
        data = Qdata(code, select_date)
        d0 = data.iloc[-1]['time_key'].split(' ')[0]
        if mod1(data, 14, 6) and mod3(data) and mod0(data):
            self.df.loc[len(self.df)] = [code, d0]
        else:
            pass
    def analyze_model4(self, code, date):
        #print(code)
        r = self.model4(code, date)
    def analyze(self):
        futures = []
        with ThreadPoolExecutor(max_workers=200) as executor:
            for i in ftid:
                futures.append(executor.submit(self.analyze_model4, i, self.date))
            kwargs = {'total': len(futures)}
            for f in tqdm(as_completed(futures), **kwargs):
                pass
    def result(self):
        print(self.df.to_string)



a = model5ft('2019-01-04')
a.analyze()


                  

                  
              
                  
