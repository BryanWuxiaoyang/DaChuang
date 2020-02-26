import time
import requests
from bs4 import BeautifulSoup
import re
import json
import sys
from datetime import datetime
import pandas as pd
import numpy as np

stockid_h=np.load('stockid_h.npy').tolist()
stockid_s=np.load('stockid_s.npy').tolist()
stockid=stockid_s+stockid_h
se=pd.Series(stockid).drop_duplicates()
#沪市A股：811+490+194=1495
#深市A股：456

start_page=1
end_page=25

stocks_info=pd.DataFrame(columns=['time','total_reads'])
for this_id in se.tolist():
    base_url='http://guba.eastmoney.com/list,'+this_id+'_{}.html'
    total_reads=0
    total_time_stamp=[]
    #print('curr stock_id')
    #print(this_id)
    #print ("\r ".format(this_id),end="")

    for page in range(start_page,end_page):
        try:
    
            #time.sleep(1)
            #print('cur page: ',page) 
            r=requests.get(base_url.format(page))
            #print(r.status_code)
            #print(r.content)
            article_list = BeautifulSoup(r.content, 'lxml').find_all(class_='articleh normal_post')
            #print('item_count: ')
            for item in article_list:
                reads=item.find_all('span',class_='l1 a1')[0].get_text()
                if '万' in reads:
                    reads=float(reads[:-1])*10000
                else:
                    reads=float(reads)
                total_reads+=reads
                time_stamp=item.find_all('span',class_='l5 a5')[0].get_text()
                total_time_stamp.append(time_stamp)
                #print(time_stamp)
        except Exception as err:
            print(err)
 
    stocks_info.loc[this_id]=[total_time_stamp,total_reads]
    break

stocks_info.to_csv('./stocks_frequency_25.csv')


import ast
from datetime import datetime
stocks_info=pd.read_csv('./stocks_frequency_25.csv',index_col=0)
new_info=pd.DataFrame(columns=['total_reads','counts','deltatime','density','RxD'],index=stocks_info.index)
for index,row in stocks_info.iterrows():
    x=ast.literal_eval(row['time'])#字符串类型list转list
    counts=len(x)
    #print(x[0])
    #注意反了
    start_time=datetime.strptime( '2019-'+x[0],'%Y-%m-%d %H:%M')
    end_time=datetime.strptime( '2019-'+x[-1],'%Y-%m-%d %H:%M')
    deltatime=(start_time-end_time).total_seconds()
    density=counts*1000/deltatime
    #print(index,row['total_reads'],counts,deltatime,density)
    new_info.loc[index]=[row['total_reads'],counts,deltatime,density,row['total_reads']*density]
new_info=new_info.sort_values(by="RxD" , ascending=False).reset_index(drop=True)
new_info.to_csv('./stocks_info_final_25.csv')