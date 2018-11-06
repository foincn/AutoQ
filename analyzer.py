#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: analyzer.py
# version: 0.1.1
# description: analyzer



from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import futuquant as ft
import pandas as pd
pd.options.mode.chained_assignment = None



q = ft.OpenQuoteContext(host='sz.omg.tf', port=11111)
# 沪深A股
hs = q.get_plate_stock('SH.3000005')[1]
# q.close()
#hs['code'] = hs['code'].map(lambda x: x[3:])
# 富途牛牛Code
ftid = hs.set_index('code').drop(columns=['stock_owner','stock_name', 'lot_size', 'stock_child_type', 'stock_type', 'list_time']).T.to_dict('records')[0]

def datechange(date, change):
    d = datetime.strptime(date,'%Y-%m-%d').date()
    new_d = d + timedelta(days=change)
    new_date = new_d.strftime('%Y-%m-%d')
    return new_date






rising_ratio = 1.04
code = 'SH.600123'
date = '2018-10-31'
start_date = datechange(date, -45)
data = q.get_history_kline(code, start=start_date, end=None, ktype=ft.KLType.K_DAY, autype=ft.AuType.QFQ)[1]
data['ma5'] = data['close'].rolling(5).mean()
data['ma10'] = data['close'].rolling(10).mean()
data['ma20'] = data['close'].rolling(20).mean()
d0 = data.iloc[-1]['time_key'].split(' ')[0]
last_close = data.iloc[-1]['close']
sum4 = data['close'][-4:].sum()
sum9 = data['close'][-9:].sum()
d0ma5p = (sum4 + last_close * rising_ratio) / 5
d0ma10p = (sum9 + last_close * rising_ratio) / 10


class model4ft():
    def __init__(self, date, rising_ratio=1.04):
        self.date = date
        self.rising_ratio = rising_ratio
        self.df = pd.DataFrame(columns=['code', 'LAST_CLOSE',  'EvenPrice', 'EvenRatio', 'd1MA5', 'd1MA10', 'd2MA5', 'd2MA10', 'd3MA5', 'd3MA10', 'MA20_raising', 'MA20_ontop', 'D0'])
    def model4(self, code, select_date, rising_ratio):
        start_date = datechange(select_date, -45)
        data = q.get_history_kline(code, start=start_date, end=select_date, ktype=ft.KLType.K_DAY, autype=ft.AuType.QFQ)[1]
        data['ma5'] = data['close'].rolling(5).mean()
        data['ma10'] = data['close'].rolling(10).mean()
        data['ma20'] = data['close'].rolling(20).mean()
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




def trend(code, date):
    end_date = datechange(date, 10)
    data = q.get_history_kline(code, start=date, end=end_date, ktype=ft.KLType.K_DAY, autype=ft.AuType.QFQ)[1]
    data = data.iloc[data[data['time_key'].isin([date+ ' 00:00:00'])].index.values[0]:].drop([0]).reset_index(drop=True)
    last_close = data.iloc[0]['last_close']
    # N1
    n1close = data.iloc[0]['close']
    n1close_rate = n1close / last_close * 100 - 100
    n1low = data.iloc[0]['low']
    n1low_rate = n1low / last_close * 100 - 100
    n1high = data.iloc[0]['high']
    n1high_rate = n1high / last_close * 100 - 100
    # N2
    n2close = data.iloc[1]['close']
    n2close_rate = n2close / last_close * 100 - 100
    n2low = data['low'].iloc[:2].min()
    n2low_rate = n2low / last_close * 100 - 100
    n2high = data['high'].iloc[:2].max()
    n2high_rate = n2high / last_close * 100 - 100
    # N3
    n3close = data.iloc[2]['close']
    n3close_rate = n3close / last_close * 100 - 100
    n3low = data['close'].iloc[:3].min()
    n3low_rate = n3low / last_close * 100 - 100
    n3high = data['close'].iloc[:3].max()
    n3high_rate = n3high / last_close * 100 - 100
    df.loc[len(df)] = [code, n1close_rate, n2close_rate, n3close_rate, n1low_rate, n2low_rate, n3low_rate, n1high_rate, n2high_rate, n3high_rate]
    #return data



ttt = trend('SH.600123', '2018-10-17')


for i in a.df['code']:
    trend(i, '2018-10-17')

'2018-10-17'



df = pd.DataFrame(columns=['code', 'N1_close%', 'N2_close%', 'N3_close%', 'N1_low%', 'N2_low%',' N3_low%', 'N1_high%', 'N2_high%', 'N3_high%'])
         
    
    
def get_trend():
    for i in a.df['code']:
        try:
            trend(i, a.date)
        except:
            print(i)










a.model4('SH.600123', '2018-10-31', 1.04)




        hist_data = data[['close', 'ma5', 'ma10', 'ma20', 'high']]
        d0 = data.index[0]
        last_close = hist_data.iloc[1]['close']
        ma4 = hist_data[0:4]['close'].mean()
        ma9 = hist_data[0:9]['close'].mean()
        d0ma5p = (ma4 * 4 + last_close * rising_ratio) / 5
        d0ma10p = (ma9 * 9 + last_close * rising_ratio) / 10
        d1ma5 = hist_data.iloc[0]['ma5']
        d1ma10 = hist_data.iloc[0]['ma10']
        d1ma20 = hist_data.iloc[0]['ma20']
        d2ma5 = hist_data.iloc[1]['ma5']
        d2ma10 = hist_data.iloc[1]['ma10']
        d2ma20 = hist_data.iloc[1]['ma20']
        d3ma5 = hist_data.iloc[2]['ma5']
        d3ma10 = hist_data.iloc[2]['ma10']
        d3ma20 = hist_data.iloc[2]['ma20']
        #print('LAST_CLOSE: %s \nd0HIGH: %s \nMA4: %s \nMA9: %s \nd0MA5p: %s \nd0MA10p: %s \nd0MA5h: %s \nd0MA10h: %s \nd1MA5: %s \nd1MA10: %s \nd2MA5: %s \nd3MA5: %s' % (last_close, d0high, ma4, ma9, d0ma5p, d0ma10p, d0ma5h, d0ma10h, d1ma5, d1ma10, d2ma5, d3ma5))
        if (d1ma5 < d1ma10) and (d2ma5 < d3ma5 < d1ma5) and (d0ma5p > d0ma10p) and (d2ma10 > d2ma5) and (d1ma10 < d2ma10):
            #print(True)
            if d1ma20 > d2ma20 > d3ma20:
                ma20_raising = True
            else:
                ma20_raising = False
            even_pirce = ma9 * 9 - ma4 * 8
            even_ratio = even_pirce / last_close - 1
            self.df.loc[len(self.df)] = [code, last_close, even_pirce, even_ratio, d1ma5, d1ma10, d2ma5, d2ma10, d3ma5, d3ma10, ma20_raising, d0]
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


    
    
