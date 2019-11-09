import requests
from bs4 import BeautifulSoup
import re
import json
import sys
from datetime import datetime
import time
#usage: 三个参数 1：起始页面 2：终止页面 3：目标股吧id

#上证指数股吧 其他股吧更改list，后面内容即可，最后大括号用于控制页数
base_url = 'http://guba.eastmoney.com/list,zssh000001_{}.html'

#遍历页码
#全部信息
records=[]
#建议一次页数少爬一点

#遍历页码
#全部信息
start_page=int(sys.argv[1])
end_page=int(sys.argv[2])
#就是'http://guba.eastmoney.com/list,zssh000001_{}.html' 里面zssh000001部分，可以用其他代替
try:
    target=sys.argv[3]
    base_url='http://guba.eastmoney.com/list,'+target+'_{}.html'
except:
    print('wrong target website or error')

records=[]

for page in range(start_page,end_page):
    try:
        time.sleep(1)
        print('cur page: ',page) 
        
        r=requests.get(base_url.format(page))
        #print(r.status_code)
        #print(r.content)
        article_list = BeautifulSoup(r.content, 'lxml').find_all(class_='articleh normal_post')
        record={}
        item_count=0
        print('item_count: ')
        for item in article_list:
            try:
                time.sleep(1)
                reads=item.find_all('span',class_='l1 a1')[0].get_text()
                title=item.find_all('span',class_='l3 a3')[0].a['title']
                href='http://guba.eastmoney.com'+item.find_all('span',class_='l3 a3')[0].a['href']
                
                detail=BeautifulSoup(requests.get(href).content, "lxml")
                data=json.loads(detail.find_all(class_='data')[0]['data-json'])

                user_id=data['user_id']
                if user_id=='':
                    user_id=-1
                else:
                    user_id=int(user_id)

                user_name=data['user_nickname']

                star=data['user_influ_level']


                time_stamp=detail.find_all(class_='zwfbtime')[0].get_text()
                time_stamp=re.sub(r'[\u4e00-\u9fa5a-zA-Z]','',time_stamp)
                
                #大部分历史数据不用计算哈希了，最近的可能爬到重复了的再计算
                #record['id']=hash(user_name+title[:5])
                record['href']=href
                record['time']=time_stamp
                record['read_count']=reads
                record['user_id']=user_id
                record['name']=user_name
                record['star']=star
                record['content']=title

                jInfo=json.dumps(record,ensure_ascii=False)

                records.append(jInfo)
                
                print ("\r ".format(item_count)+str(item_count), end="")
                item_count+=1
            except:
                print('error at item, ',item_count)
            
    except:
        print('error at page: ',page)
    

print('\ntotal records', len(records))

outPath="./"+target+'_'+str(start_page)+'-'+str(end_page)+'.json'

with open(outPath, 'w', encoding='utf-8') as fout:
    fout.write('[\n')
    for i in records[:-1]:
        i+=',\n'
        fout.write(i)
    fout.write(records[-1]+'\n')
    fout.write(']')