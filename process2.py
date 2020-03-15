import pandas as pd
#自行定义函数并添加到filteres中，建议判断条件保守一点？
#positive comment:2  negtive:0 neutral:1 
def neg_word_filter(data):
    neg_words=['垃圾','下跌','闪崩','无耻','下行','跌停','很差','绿了',
    '沙必','马蛋','没救了','崩盘','守不住','跳水']
    for i,row in data.iterrows():
        if row['label']==9:
            for this_word in neg_words:
                if this_word in str(row['content']):
                    data.loc[i,'label']=0
                    data.loc[i,'reason']='neg_word: '+this_word
                    print('find neg_word'+this_word+' and label it 0')
                    break
    return data


def label_statistic(data):
    #x=data.label.value_counts()
    x=data[data['label']==9]
    print('now labeled: ',len(x)/len(data))

filters=[neg_word_filter]

if __name__ == '__main__':
    data = pd.read_csv('./comment_all1.csv',index_col=0)#.iloc[:100]
    for i in filters:
        data = i(data)
    label_statistic(data)
    data.to_csv('./temp.csv')