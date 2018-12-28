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



def Qdata(code, date, future=False):
    start_date = datechange(date, -45)
    data = q.get_history_kline(code, start=start_date, end=date, ktype=ft.KLType.K_DAY, autype=ft.AuType.QFQ)[1]
    data['ma5'] = data['close'].rolling(5).mean()
    data['ma10'] = data['close'].rolling(10).mean()
    data['ma15'] = data['close'].rolling(15).mean()
    data['ma20'] = data['close'].rolling(20).mean()
    return data



def mod1(data, day=8)
    d1ma5 = data.iloc[-1]['ma5']
    d2ma5 = data.iloc[-2]['ma5']
    d3ma5 = data.iloc[-3]['ma5']
    d4ma5 = data.iloc[-4]['ma5']
    d5ma5 = data.iloc[-5]['ma5']
    d6ma5 = data.iloc[-6]['ma5']
    d7ma5 = data.iloc[-7]['ma5']
    d8ma5 = data.iloc[-8]['ma5']
    d1ma10 = data.iloc[-1]['ma10']
    d2ma10 = data.iloc[-2]['ma10']
    d3ma10 = data.iloc[-3]['ma10']
    d4ma10 = data.iloc[-4]['ma10']
    d5ma10 = data.iloc[-5]['ma10']
    d6ma10 = data.iloc[-6]['ma10']
    d7ma10 = data.iloc[-7]['ma10']
    d8ma10 = data.iloc[-8]['ma10']
    d1ma15 = data.iloc[-1]['ma15']
    d2ma15 = data.iloc[-2]['ma15']
    d3ma15 = data.iloc[-3]['ma15']
    d4ma15 = data.iloc[-4]['ma15']
    d5ma15 = data.iloc[-5]['ma15']
    d6ma15 = data.iloc[-6]['ma15']
    d7ma15 = data.iloc[-7]['ma15']
    d8ma15 = data.iloc[-8]['ma15']
    d1ma20 = data.iloc[-1]['ma20']
    d2ma20 = data.iloc[-2]['ma20']
    d3ma20 = data.iloc[-3]['ma20']
    d4ma20 = data.iloc[-4]['ma20']
    d5ma20 = data.iloc[-5]['ma20']
    d6ma20 = data.iloc[-6]['ma20']
    d7ma20 = data.iloc[-7]['ma20']
    d8ma20 = data.iloc[-8]['ma20']
    if (d1ma5 < d1ma10 < d1ma20





class model4ft():
    def __init__(self, date, rising_ratio=1.04):
        self.date = date
        self.rising_ratio = rising_ratio
        self.df = pd.DataFrame(columns=['code', 'LAST_CLOSE',  'EvenPrice', 'EvenRatio', 'd1MA5', 'd1MA10', 'd2MA5', 'd2MA10', 'd3MA5', 'd3MA10', 'MA20_raising', 'MA20_ontop', 'D0'])
    def model4(self, code, select_date, rising_ratio):
        start_date = datechange(select_date, -45)
        data = Qdata(code, select_date)
        d0 = data.iloc[-1]['time_key'].split(' ')[0]
        last_close = data.iloc[-1]['close']
        d1ma5 = data.iloc[-1]['ma5']
        d2ma5 = data.iloc[-2]['ma5']
        d3ma5 = data.iloc[-3]['ma5']
        d1ma10 = data.iloc[-1]['ma10']
        d2ma10 = data.iloc[-2]['ma10']
        d3ma10 = data.iloc[-3]['ma10']
        d1ma20 = data.iloc[-1]['ma20']
        d2ma20 = data.iloc[-2]['ma20']
        d3ma20 = data.iloc[-3]['ma20']
        sum4 = data['close'][-4:].sum()
        sum9 = data['close'][-9:].sum()
        d0ma5p = (sum4 + last_close * rising_ratio) / 5
        d0ma10p = (sum9 + last_close * rising_ratio) / 10
        if (d1ma5 < d1ma10) and (d2ma5 < d3ma5 < d1ma5) and (d0ma5p > d0ma10p) and (d2ma10 > d2ma5) and (d1ma10 < d2ma10):
            #print(True)
            if d1ma20 > d2ma20 > d3ma20:
                ma20_raising = True
            else:
                ma20_raising = False
            if d1ma20 > d1ma10:
                ma20_ontop = True
            else:
                ma20_ontop = False
            even_pirce = sum9 - sum4 * 2
            even_ratio = even_pirce / last_close - 1
            self.df.loc[len(self.df)] = [code, last_close, even_pirce, even_ratio, d1ma5, d1ma10, d2ma5, d2ma10, d3ma5, d3ma10, ma20_raising, ma20_ontop, d0]
        else:
            pass
    def analyze_model4(self, code, date, rising_ratio):
        #print(code)
        r = self.model4(code, date, rising_ratio)
    def analyze(self):
        futures = []
        with ThreadPoolExecutor(max_workers=200) as executor:
            for i in ftid:
                futures.append(executor.submit(self.analyze_model4, i, self.date, self.rising_ratio))
            kwargs = {'total': len(futures)}
            for f in tqdm(as_completed(futures), **kwargs):
                pass
    def result(self):
        print(self.df.to_string)



a = model4ft('2018-07-05')
a.analyze()

