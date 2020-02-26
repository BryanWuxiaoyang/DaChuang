import requests
from bs4 import BeautifulSoup
import re
import json
import sys
from datetime import datetime
import time
import numpy as np
import pandas as pd
stkcd=np.load('stkcd.npy').tolist()
#stkcd=stkcd[:1]

start_page=1#int(sys.argv[1])
end_page=40#int(sys.argv[2])

for i in list(range(0,len(stkcd),500)):
    k=1
    df=pd.DataFrame()
    
    for this_id in stkcd[i:i+500]:
        base_url='http://guba.eastmoney.com/list,'+this_id+'_{}.html'
        print(this_id)
        for page in list(range(start_page,end_page)):
            try:
                time.sleep(1)
                print('cur page: ',page) 
                r=requests.get(base_url.format(page))
                article_list = BeautifulSoup(r.content, 'lxml').find_all(class_='articleh normal_post')
                item_count=0
                #print('item_count: ')
                for item in article_list:
                    try:
                        time.sleep(0.1)
                        reads=item.find_all('span',class_='l1 a1')[0].get_text()
                        #title=item.find_all('span',class_='l3 a3')[0].a['title']
                        href='http://guba.eastmoney.com'+item.find_all('span',class_='l3 a3')[0].a['href']
                        detail=BeautifulSoup(requests.get(href).content, "lxml")
                        title=detail.find_all('div',id='zwconttbt')[0].get_text()
                        data=json.loads(detail.find_all(class_='data')[0]['data-json'])
                        user_id=data['user_id']
                        if user_id=='':
                            user_id=-1
                        else:
                            user_id=int(user_id)
                        #user_name=data['user_nickname']
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
                        pass
                        #print(err)
                    
            except Exception as err:
                pass
                #print(err)
    df.to_csv('./comment'+str(k)+'.csv' )
    k+=1   



