# -*- coding: utf-8 -*-

'''如果最后有数据和最开始获取的url的数目不一样,原因可能是中间有的数据没有获取到,在怀疑有问题的数据前加上response.url判断下到哪条数据出错'''

import json
import re
import scrapy
from Lianjiaspider.items import LianjiaspiderItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://hf.lianjia.com/ershoufang']

    def parse(self, response):
        node_list = response.xpath('//div[@class="leftContent"]/ul/li[@class="clear"]')
        # print(len(node_list))
        for node in node_list:
            item = LianjiaspiderItem()

            item['link'] = node.xpath('./div[1]/div[1]/a/@href').extract_first()
            # print(item)
            yield scrapy.Request(
                item['link'],
                callback=self.parse_detail,
                meta={'meta1':item}
            )

        # next_url = 'https://hf.lianjia.com' + response.xpath('//div[@class="page-box house-lst-page-box"]/a[last()]/@href').extract[0]
        # if response.xpath('//div[@class="page-box house-lst-page-box"]/a[last()]') is not None:
        #     yield scrapy.Request(next_url,callback=self.parse)

        #page_url = /ershoufang/pg{page}/
        page_url = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract_first()
        #page_data = {"totalPage":100,"curPage":1}
        page_data = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract_first()

        totalPage = int(re.search(r'"totalPage":(\d+)',page_data).group(1))
        for total_page in range(2,totalPage+1):
            next_url = 'https://hf.lianjia.com' + page_url.format(page=total_page)
            yield scrapy.Request(next_url, callback=self.parse)
            # print('***********',next_url)

        # print('++++++++++',page_url,page_data)

    def parse_detail(self,response):
        # print(response.url)
        item = response.meta['meta1']
        item['title'] = response.xpath('//div[@class="title"]/h1/text()').extract_first()
        item['total_price'] = response.xpath('//div[@class="price "]/span[1]/text()').extract_first() + '万'
        item['unit_price'] = response.xpath('//div[@class="unitPrice"]/span/text()').extract_first() + '元/平米'
        item['down_payment'] = ''.join(response.xpath('//div[2]/span[@class="taxtext"]/span[1]/text()').extract()).split()
        item['specifications'] = response.xpath('//div[@class="room"]/div[1]/text()').extract_first()
        item['floor_info'] = response.xpath('//div[@class="room"]/div[2]/text()').extract_first()

        item['toward'] = ''.join(response.xpath('//div[@class="type"]/div/text()').extract())
        item['size'] = response.xpath('//div[@class="area"]/div[1]/text()').extract_first()
        item['build_time'] = response.xpath('//div[@class="area"]/div[2]/text()').extract_first()
        item['community_name'] = response.xpath('//div[@class="communityName"]/a[1]/text()').extract_first()
        item['area'] = response.xpath('//div[@class="areaName"]/span[2]/a/text()').extract()
        item['viewing_time'] = response.xpath('//div[@class="visitTime"]/span[2]/text()').extract_first()
        item['lianjia_num'] = response.xpath('//div[@class="houseRecord"]/span[2]/text()').extract_first()
        item['contant_name'] = response.xpath('//div[@class="brokerInfoText fr"]/div[1]/a[1]/text()').extract_first()
        item['contant_phone'] = '转'.join(response.xpath('//div[@class="brokerInfoText fr"]/div[3]/text()').extract())
        bi =  response.xpath('//div[@class="base"]//ul/li/span/text()|//div[@class="base"]//ul/li/text()').extract()
        # 用列表推导式将列表中的1和2取出用:拼接
        item['basic_info'] =[bi[i].strip()+':'+bi[i+1].strip() for i in range(0,len(bi),2)]
        # print(item['basic_info'])
        #用:拼接,会将所有的都用:拼接起来,不可行
        # item['transaction_info'] = ':'.join(response.xpath('//div[@class="transaction"]//ul/li/span/text()').extract())
        ti = response.xpath('//div[@class="transaction"]//ul/li/span/text()').extract()
        item['transaction_info'] = [ti[i].strip()+':'+ti[i+1].strip() for i in range(0,len(ti),2)]

        # item['housing_characteristics'] = ''.join(response.xpath('//div[@class="newwrap baseinform"][2]/div/div/div/text()|//div[@class="newwrap baseinform"][2]/div/div/div//a/text()').extract()).replace('\n','').strip()
        hc = response.xpath('//div[@class="newwrap baseinform"][2]/div/div/div/text()|//div[@class="newwrap baseinform"][2]/div/div/div//a/text()').extract()
        item['housing_characteristics'] = [hc[i].strip()+':'+hc[i+1].strip() for i in range(0,len(hc),2)]


        # item['house_type'] = response.xpath('//*[@id="infoList"]/div/div/text()').extract()

        ht = response.xpath('//*[@id="infoList"]/div/div/text()').extract()
        # print(ht)

        #不能格式化输出
        # htt = [ht[i] for i in range(0,len(ht),4)]
        # item['house_type'] = [htt[i].strip()+':'+htt[i+1].strip()+','+htt[i+2].strip()+','+htt[i+3].strip() for i in range(len(htt))]

        #格式化输出,将ht中的所有数据遍历,以4为倍数,取出组数,取出第1个.第5个.第9个...依次取出,然后第2个.第3个.第4个用i+1,i+2,i+3得出
        item['house_type'] = [ht[i].strip()+':'+ht[i+1].strip()+','+ht[i+2].strip()+','+ht[i+3].strip() for i in range(0,len(ht),4)]

        item['house_photo'] = response.xpath('//div[@class="container"]/div/div/img/@src').extract()
        # ci = response.xpath('//*[@id="resblockCardContainer"]/div/div/div[2]/div/div/label/text()|//*[@id="resblockCardContainer"]/div/div/div[2]/div/div/span/text()|//*[@id="resblockCardContainer"]/div/div/div[2]/div/div/span/a/text()').extract()

        # with open('hh.html','wb') as f:
        #     f.write(response.body)

        # ci = response.xpath('//*[@id="resblockCardContainer"]/div/div/div[2]/div/div/label/text()|//*[@id="resblockCardContainer"]/div/div/div[2]/div/div/span/text()').extract()
        #
        # print(ci)
        # item['community_info'] = [ci[i].strip()+':'+ci[i+1].strip() for i in range(0,len(ci),2)]
        # print(item)
        #rid,hid在网页源码中有切只有一处,所以用search匹配,   .group(1)用来获取匹配到的第二个值
        rid = re.search(r"resblockId:'(\d+)'",response.text).group(1)
        hid = re.search(r"houseId:'(\d+)'",response.text).group(1)
        # print(rid,hid)
        # url = 'https://hf.lianjia.com/ershoufang/housestat?hid=103102081498&rid=5111062454890'
        url = 'https://hf.lianjia.com/ershoufang/housestat?hid='+hid+ '&rid='+rid

        yield scrapy.Request(
            url=url,
            callback=self.parse_ci,
            meta={'meta2': item}
        )

    def parse_ci(self,response):
        item = response.meta['meta2']
        dict_data = json.loads(response.text)
        #将数据格式化方便查看结构
        str_data = json.dumps(json.loads(response.body.decode()),ensure_ascii=False)
        # print(str_data)

        temp = {}
        temp['name']= dict_data['data']['resblockCard']['name']
        temp['unitPrice']= dict_data['data']['resblockCard']['unitPrice']
        temp['buildYear']= dict_data['data']['resblockCard']['buildYear']
        temp['buildType']= dict_data['data']['resblockCard']['buildType']
        temp['buildNum']= dict_data['data']['resblockCard']['buildNum']
        temp['frameNum']= dict_data['data']['resblockCard']['frameNum']
        temp['sellNum']= dict_data['data']['resblockCard']['sellNum']
        temp['rentNum']= dict_data['data']['resblockCard']['rentNum']

        item['community_info'] = temp

        print('-------',item)
        # print('-------',item['title'])
        yield item
