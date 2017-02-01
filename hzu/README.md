# scrapy_hzu
利用scrapy模拟登陆惠州学院教务处，爬取学生信息，再利用anaconda进行数据分析`惠州学院`

### 运行命令：

```python
scrapy crawl jwc_01					#爬取全校各班学号为01的学生信息存储至hzu.xls
scrapy crawl jwc_all -o jwc_all.json#爬取全校学生信息
```

目前爬取的是12~15级的学生信息，几个小时爬取完毕，获取了15232名同学信息，下一步进行分析。