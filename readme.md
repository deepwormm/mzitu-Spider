# mzitu-spider

刚开始学 scrapy，写了一个小玩具，可以爬取 mzitu 的所有图片

## 环境

scrpy1.6.0
requests2.22.0
python3.6.0

## 使用

在 example.py 第 32 行修改为自己的本地存储路径  
cd mizitu  
scrapy crawl mzitu  

## 功能/特点

- 按照时间顺序，从后往前线性爬取套图(先爬最新的)
- 图片的存储没有使用 pipeline，直接写了一个函数，用 requests 下载到本地(刚开始学没用 pipeline,下次肯定会用)
- 图片存储在本地时线性存储，所有套图的所有图片都存储在同一个文件夹下，图片量大之后会造成文件夹非常臃肿（烧内存的那种）
- 在每组套图下载完之后，会在本地存一个*9999*.jpg 文件，里面存的是一些无意义的数据，只做一个标志，因为没有用数据库，觉得这么方便就这么弄了。
- 因为会做创建一个*9999*.jpg 文件，所以有了标志，至少可以在更新图库的时候不用再重新下载了。

## 缺陷

- 由于在写这个的时候试了一个代理池，代理池的使用就一直留在代码里没删，其实不影响，删了也行
- 32 行有个路径是我自己的。。。。
