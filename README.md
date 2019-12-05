# DaChuang
#### 这是VoidFly 的分支

guba_spider.py
usage： 三个参数 1.start_page 2.end_page 3.股吧id

## 每一只股票股吧信息频率统计
文件  stocks_info_final.csv
统计了每一只股票（沪+深，且剔除沪市b股）股吧前五页数据
读取请用read_csv(,index_col=0) index为股票id （int类型，可能需要转换）

- total_reads: 所有贴子阅读数综合
- counts：贴子数综合
- deltatime：最早帖子和最晚帖子时间差 单位s
- density：counts/deltatime

stockid_h 和stockid_s 分别为统计的股票列表 沪深两市，其中深市包含中小板、创业版、可能需要剔除
  