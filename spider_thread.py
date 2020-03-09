import requests
requests.adapters.DEFAULT_RETRIES = 5 #增加重连次数
from bs4 import BeautifulSoup
import re
import json
import sys
from datetime import datetime
import time
import numpy as np
import pandas as pd
import random
import threading
#threading.TIMEOUT_MAX=5
from queue import Queue
stkcd=np.load('stkcd.npy').tolist()
#stkcd=stkcd[200:]

start_page=1#int(sys.argv[1])
end_page=40#int(sys.argv[2])

proxy_list=[{"http":'http://60.217.64.237:31923'},{'http':'http://115.223.120.254:8010'},
{'http':'http://117.88.177.174:3000'},{"https":'https://117.88.176.63:3000'},{'https':'https://49.65.160.69:18118'},
{'http':'http://117.88.253.225:8118'},{'http':'http://110.73.8.171:8123'},{'http':'http://61.135.155.82:443'},
{'https':'https://117.88.176.186:3000'},{'http':'http://222.95.144.183:3000'},{'http':'http://121.237.148.16:3000'}]


def get_detail(detail_list,dct_queue,i):
    s=requests.session()#
    s.keep_alive=False#防止维持的链接过多
    while(not detail_list.empty()):
        try:
            #print('thread {} working'.format(i))
            time.sleep(0.3)
            item=detail_list.get()

            reads=item.find_all('span',class_='l1 a1')[0].get_text()
            comments=item.find_all('span',class_='l2 a2')[0].get_text()

            href='http://guba.eastmoney.com'+item.find_all('span',class_='l3 a3')[0].a['href']

            detail=BeautifulSoup(s.get(href,headers={'Connection':'close'}).content, "lxml")#在请求报头里面写明关闭链接

            title=detail.find_all('div', class_='stockcodec .xeditor')[0].get_text().strip()

            if len(title)>300:
            	continue

            
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
            record['comment_count']=comments
            
            dct_queue.put(record)
        except Exception as err:
            #pass
            print(err)



k=1
step=10
for i in list(range(0,len(stkcd),step)):
    df=pd.DataFrame()
    m=1
    for this_id in stkcd[i:i+step]:
        base_url='http://guba.eastmoney.com/list,'+this_id+'_{}.html'
        print('num of stocks: ',m)
        m+=1
        print(this_id)
        for page in list(range(start_page,end_page)):
            try:
                time.sleep(1)
                print('cur page: ',page) 
            
                #proxy=random.choice(proxy_list)

                s=requests.session()
                s.keep_alive=False

                r=s.get(base_url.format(page),headers={'Connection':'close'})#,proxies=proxy)
                article_list = BeautifulSoup(r.content, 'lxml').find_all(class_='articleh normal_post')
                item_count=0
                #print('item_count: ')

                detail_url_queue = Queue(maxsize=200)#每一页要爬取
                for item in article_list:
                    detail_url_queue.put(item)

                dct_queue=Queue(maxsize=200)#每一页已爬取
                
                #设置线程数
                num_of_threads=3


                ths=[]#初始化线程
                for i in range(num_of_threads):
                    th=threading.Thread(target=get_detail,args=(detail_url_queue,dct_queue,i))
                    ths.append(th)

                #start_time = time.time()
                for i in range(num_of_threads):
                    #ths[i].setDaemon(True)
                    ths[i].start()
                for i in range(num_of_threads):
                    ths[i].join(5)#设置timeout

                
                while(not dct_queue.empty()):
                    r=dct_queue.get()
                    df=df.append(pd.DataFrame(r,index=[this_id]))
                    
                print('df len: ',len(df))    
                detail_url_queue.queue.clear()
                dct_queue.queue.clear()
                    
            except Exception as err:
                #pass
                print(err)
    df.to_csv('./comment'+str(k)+'.csv' )
    del df
    k+=1   



