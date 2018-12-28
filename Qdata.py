#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: analyzer.py
# version: 0.1.1
# description: analyzer


import futuquant as ft
import pandas as pd
pd.options.mode.chained_assignment = None


from datetime import datetime, timedelta

def datechange(date, change):
    d = datetime.strptime(date,'%Y-%m-%d').date()
    new_d = d + timedelta(days=change)
    new_date = new_d.strftime('%Y-%m-%d')
    return new_date



def Qdata(ftcode, date, future=False):
    start_date = datechange(date, -55)
    data = q.get_history_kline(ftcode, start=start_date, end=date, ktype=ft.KLType.K_DAY, autype=ft.AuType.QFQ)[1]
    data['ma5'] = data['close'].rolling(5).mean()
    data['ma10'] = data['close'].rolling(10).mean()
    data['ma15'] = data['close'].rolling(15).mean()
    data['ma20'] = data['close'].rolling(20).mean()
    return data



def mod1(data, day=8):
    result = False
    for d in range(day):
        i = - (d + 1)
        ma5 = data.iloc[i]['ma5']
        ma10 = data.iloc[i]['ma10']
        ma15 = data.iloc[i]['ma15']
        ma20 = data.iloc[i]['ma20']
        if ma5 < ma10 < ma20:
            if d + 1 == day:
                result = True
        else:
            break
    return result


def mod2(data):
    d1ma5 = data.iloc[-1]['ma5']
    d2ma5 = data.iloc[-2]['ma5']
    d3ma5 = data.iloc[-3]['ma5']
    if d1ma5 > d3ma5 > d2ma5: 
        result = True
    return result




df = pd.DataFrame(columns=['code', 'date']

                  
               
       



class model4ft():
    def __init__(self, date, day=8):
        self.date = date
        self.day = day
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



a = model4ft('2016-10-10')
a.analyze()

