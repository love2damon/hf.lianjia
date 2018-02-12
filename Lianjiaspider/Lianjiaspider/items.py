# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 标题
    title = scrapy.Field()
    # 房屋链接
    link = scrapy.Field()
    # 总价格
    total_price = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 首付
    down_payment = scrapy.Field()
    # 规格
    specifications = scrapy.Field()
    # 楼层信息
    floor_info = scrapy.Field()
    # 朝向
    toward = scrapy.Field()
    # 大小
    size = scrapy.Field()
    # 建造时间
    build_time = scrapy.Field()
    # 小区名称
    community_name = scrapy.Field()
    # 所在区域
    area = scrapy.Field()
    # 看房时间
    viewing_time = scrapy.Field()
    # 链家编号
    lianjia_num = scrapy.Field()
    # 联系人
    contant_name = scrapy.Field()
    # 联系人电话
    contant_phone = scrapy.Field()
    # 基本信息
    basic_info = scrapy.Field()
    #交易属性
    transaction_info = scrapy.Field()
    # 房源特色
    housing_characteristics = scrapy.Field()
    # 户型分间
    house_type = scrapy.Field()
    # 房源照片
    house_photo = scrapy.Field()
    # 小区简介
    community_info = scrapy.Field()
    pass