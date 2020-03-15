import pandas as pd
df=pd.DataFrame()
for i in range(25):
    x=pd.read_csv('allData1/comment{}.csv'.format(i+1),index_col=0)
    df=df.append(x)
df=df.reset_index().rename(columns={'index':'stkcd'})
df['label']=9
df['reason']=' '
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
x=df['content'].apply(lambda x: not is_number(x))
df=df[x]
df=df.reset_index(drop=True)
df.to_csv('./comment_all1.csv')