import requests
from bs4 import BeautifulSoup
import re
import json
import sys
from datetime import datetime
import time
import numpy as np
import pandas as pd
#usage: 三个参数 1：起始页面 2：终止页面 3：目标股吧id

#上证指数股吧 其他股吧更改list，后面内容即可，最后大括号用于控制页数
#base_url = 'http://guba.eastmoney.com/list,zssh000001_{}.html'

stkcd=np.load('stkcd.npy').tolist()
#stkcd=stkcd[:1]


#records=[]
#遍历页码
start_page=1#int(sys.argv[1])
end_page=60#int(sys.argv[2])
#就是'http://guba.eastmoney.com/list,zssh000001_{}.html' 里面zssh000001部分，可以用其他代替


#target=sys.argv[3]
#base_url='http://guba.eastmoney.com/list,'+target+'_{}.html'

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
                        #大部分历史数据不用计算哈希了，最近的可能爬到重复了的再计算
                        #record['id']=hash(user_name+title[:5])
                        #record['href']=href
                        record={}
                        #record['stkcd']=this_id
                        record['time']=time_stamp
                        record['read_count']=reads
                        record['user_id']=user_id
                        #record['name']=user_name
                        record['star']=star
                        record['content']=title
                        #jInfo=json.dumps(record,ensure_ascii=False)
                        #print(record)
                        df=df.append(pd.DataFrame(record,index=[this_id]))
                        #print(df)
                        #print ("\r ".format(item_count)+str(item_count), end="")
                        #item_count+=1
                        #break
                    except Exception as err:
                        pass
                        #print(err)
                    
            except Exception as err:
                pass
                #print(err)
    df.to_csv('./comment'+str(k)+'.csv' )
    k+=1   



