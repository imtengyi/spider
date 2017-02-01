# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field

class HzuItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 姓名
    stu_name = Field()
    # 学号
    stu_num= Field()
    # 性别
    stu_sex = Field()
    # 生日
    stu_birth = Field()
    # 民族
    stu_nation = Field()
    # 年级
    stu_grade = Field()
    # 系别
    stu_department = Field()
    # 专业
    stu_major = Field()
    # 班级
    stu_classes = Field()
    # 电话
    stu_tel = Field()
    # 身份证
    stu_identify = Field()
    # 学生类型
    stu_type = Field()
    # 家庭地址
    stu_address = Field()
    # 籍贯
    stu_native_place = Field()
    # 生源地
    stu_origin_address = Field()







