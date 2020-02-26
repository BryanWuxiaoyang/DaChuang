import requests
requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
from bs4 import BeautifulSoup
import re
import json
import sys
from datetime import datetime
import time
import numpy as np
import pandas as pd
import random
stkcd=np.load('stkcd.npy').tolist()
#stkcd=stkcd[:1]

start_page=1#int(sys.argv[1])
end_page=36#int(sys.argv[2])

proxy_list=[{"http":'http://60.217.64.237:31923'},{'http':'http://115.223.120.254:8010'},
{'http':'http://117.88.177.174:3000'},{"https":'https://117.88.176.63:3000'},{'https':'https://49.65.160.69:18118'},
{'http':'http://117.88.253.225:8118'},{'http':'http://110.73.8.171:8123'},{'http':'http://61.135.155.82:443'},
{'https':'https://117.88.176.186:3000'},{'http':'http://222.95.144.183:3000'},{'http':'http://121.237.148.16:3000'}]


s=requests.session()
s.keep_alive=False
k=1
for i in list(range(0,len(stkcd),100)):#500只保存一次
    
    df=pd.DataFrame()
    m=1
    for this_id in stkcd[i:i+100]:
        base_url='http://guba.eastmoney.com/list,'+this_id+'_{}.html'
        print('num of stocks: ',m)
        m+=1
        print(this_id)
        for page in list(range(start_page,end_page)):
            try:
                time.sleep(1)
                print('cur page: ',page) 
                proxy=random.choice(proxy_list)
                
                r=s.get(base_url.format(page),proxies=proxy)
                article_list = BeautifulSoup(r.content, 'lxml').find_all(class_='articleh normal_post')
                item_count=0
                #print('item_count: ')
                for item in article_list:
                    try:
                        time.sleep(0.5)
                        reads=item.find_all('span',class_='l1 a1')[0].get_text()
                        href='http://guba.eastmoney.com'+item.find_all('span',class_='l3 a3')[0].a['href']
                        detail=BeautifulSoup(requests.get(href).content, "lxml")
                        title=detail.find_all('div',id='zwconttbt')[0].get_text()
                        data=json.loads(detail.find_all(class_='data')[0]['data-json'])
                        user_id=data['user_id']
                        if user_id=='':
                            user_id=-1
                        else:
                            user_id=int(user_id)
                      
                        star=data['user_influ_level']
                        time_stamp=detail.find_all(class_='zwfbtime')[0].get_text()
                        time_stamp=re.sub(r'[\u4e00-\u9fa5a-zA-Z]','',time_stamp)
                        #record['id']=hash(user_name+title[:5])                
                        record={}
                        record['time']=time_stamp
                        record['read_count']=reads
                        record['user_id']=user_id                       
                        record['star']=star
                        record['content']=title
                        
                        df=df.append(pd.DataFrame(record,index=[this_id]))
                        
                    except Exception as err:
                        #pass
                        print(err)
                    
            except Exception as err:
                #pass
                print(err)
    df.to_csv('./comment'+str(k)+'.csv' )
    k+=1   



