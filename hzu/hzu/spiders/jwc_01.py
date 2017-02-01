#-*- coding: utf-8 -*
__author__ = 'Howie'
from scrapy.http import Request,FormRequest
from scrapy.spider import Spider
from scrapy.selector import Selector
from xlwt import *
from hzu.items import HzuItem

class jwcSpider(Spider):
    name = "jwc_01"
    login_page = "http://202.192.224.137/"
    start_urls = ["http://202.192.224.137/main.aspx",
                  "http://202.192.224.137/xsxx.aspx?xh="]
    hzu_work = Workbook(encoding='utf-8')
    hzu_sheet = hzu_work.add_sheet('hzu_jwc')
    line = 0

    def start_requests(self):
        return [Request(self.login_page,callback=self.post_login)]

    def post_login(self,response):
        viewstate = Selector(response).xpath('//input[@name="__VIEWSTATE"]/@value').extract()[0]
        return [FormRequest.from_response(response,
                                          formdata={
                                              '__VIEWSTATE':viewstate,
                                              'yh':'xh',
                                              'kl':'pass',
                                              'RadioButtonList1':'学生',
                                              'Button1':'登  录',
                                              'CheckBox1': 'on'
                                          },
                                          callback=self.logged_in)]
    def logged_in(self,response):
        return [Request(self.start_urls[0],self.get_page)]

    def get_page(self, response):
        #因为学校学号没有规律，因此爬取每个班学号为01的学生信息，存储在hzu.xls文件中
        year = ['12', '13', '14', '15']
        department = ['11', '12', '13', '14', '23', '24','26','01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
        third = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']
        four = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26']
        head = []
        tail = []
        for tail_1 in four:
            for tail_2 in range(1, 27):
                tail.append(tail_1+str('%02d' % tail_2))
        self.hzu_sheet.write(0, 0, '姓名')
        self.hzu_sheet.write(0, 1, '学号')
        self.hzu_sheet.write(0, 2, '性别')
        self.hzu_sheet.write(0, 3, '生日')
        self.hzu_sheet.write(0, 4, '民族')
        self.hzu_sheet.write(0, 5, '年级')
        self.hzu_sheet.write(0, 6, '系别')
        self.hzu_sheet.write(0, 7, '专业')
        self.hzu_sheet.write(0, 8, '班级')
        self.hzu_sheet.write(0, 9, '电话')
        self.hzu_sheet.write(0, 10, '身份证')
        self.hzu_sheet.write(0, 11, '学生类型')
        self.hzu_sheet.write(0, 12, '家庭地址')
        self.hzu_sheet.write(0, 13, '籍贯')
        self.hzu_sheet.write(0, 14, '生源地')
        for head_0 in year:
            for head_1 in department:
                for head_2 in third:
                    head.append(head_0 + head_1 + head_2)
        for head_3 in head:
            for tail_3 in tail:
                head_4 = head_3 + tail_3 + "101"
                yield self.make_requests_from_url(self.start_urls[1] + str(head_4))

    def parse(self, response):
        item = HzuItem()
        result = Selector(response)
        if result.xpath('//td/span[@id="xm"]/text()').extract():
            item['stu_name'] = result.xpath('//td/span[@id="xm"]/text()').extract()[0]
            item['stu_num'] = result.xpath('//td/span[@id="xh"]/text()').extract()[0]
            item['stu_sex'] = result.xpath('//td/span[@id="xb"]/text()').extract()[0]
            item['stu_birth'] = result.xpath('//td/span[@id="csrq"]/text()').extract()[0]
            item['stu_nation'] = result.xpath('//td/span[@id="mz"]/text()').extract()[0]
            item['stu_grade'] = result.xpath('//td/span[@id="dqszj"]/text()').extract()[0]
            item['stu_department'] = result.xpath('//td/span[@id="xymc"]/text()').extract()[0]
            item['stu_major'] = result.xpath('//td/span[@id="zymc"]/text()').extract()[0]
            item['stu_classes'] = result.xpath('//td/span[@id="bjmc"]/text()').extract()[0]
            item['stu_tel'] = result.xpath('//td/span[@id="lxdh"]/text()').extract()[0]
            item['stu_identify'] = result.xpath('//td/span[@id="sfzh"]/text()').extract()[0]
            item['stu_type'] = result.xpath('//span[@id="kslb"]/text()').extract()[0]
            item['stu_address'] = result.xpath('//td/span[@id="jtdz"]/text()').extract()[0]
            item['stu_native_place'] = result.xpath('//td/span[@id="jg"]/text()').extract()[0]
            item['stu_origin_address'] = result.xpath('//td/span[@id="syszd"]/text()').extract()[0]
            self.line += 1
            self.hzu_sheet.write(self.line, 0, item['stu_name'])
            self.hzu_sheet.write(self.line, 1, item['stu_num'])
            self.hzu_sheet.write(self.line, 2, item['stu_sex'])
            self.hzu_sheet.write(self.line, 3, item['stu_birth'])
            self.hzu_sheet.write(self.line, 4, item['stu_nation'])
            self.hzu_sheet.write(self.line, 5, item['stu_grade'])
            self.hzu_sheet.write(self.line, 6, item['stu_department'])
            self.hzu_sheet.write(self.line, 7, item['stu_major'])
            self.hzu_sheet.write(self.line, 8, item['stu_classes'])
            self.hzu_sheet.write(self.line, 9, item['stu_tel'])
            self.hzu_sheet.write(self.line, 10, item['stu_identify'])
            self.hzu_sheet.write(self.line, 11, item['stu_type'])
            self.hzu_sheet.write(self.line, 12, item['stu_address'])
            self.hzu_sheet.write(self.line, 13, item['stu_native_place'])
            self.hzu_sheet.write(self.line, 14, item['stu_origin_address'])
            self.hzu_work.save('hzu.xls')
            return item


