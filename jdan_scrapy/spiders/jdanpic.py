# -*- coding: utf-8 -*-
import scrapy
from jdan_scrapy.items import JdanScrapyItem


class JdanpicSpider(scrapy.Spider):
    name = "jdanpic"
    allowed_domains = ["jandan.net"]
    start_urls = (
        'http://www.jandan.net/pic',
    )

    handle_httpstatus_list = [403]
    page_crawled = 0

    def parse(self, response):
        if response.status == 403:
            print 'handling 403'
            rebody = scrapy.Selector(text=response.body)
            input_from = rebody.xpath('//input[@name="from"]/@value').extract()[0]
            input_hash = rebody.xpath('//input[@name="hash"]/@value').extract()[0]
            print input_from
            url = "http://www.jandan.net/block.php?action=check_human"
            yield scrapy.FormRequest(url,method="POST",
                    formdata={"from":input_from, "hash":input_hash},
                    callback=self.parse)
            return 

        next_page = response.xpath(
                '//span[@class="current-comment-page"]/following-sibling::*[1]')[0]\
                        .xpath('@href').extract()[0]


        for pic_section in response.xpath('//ol[@class="commentlist"]/li'):
            #print pic_section.extract()
            flag = pic_section.xpath('.//div[@class="author"]')
            #print flag
            if len(flag) == 0:
                continue
            author = pic_section.xpath('.//strong/text()').extract()[0] if len(pic_section.xpath('.//strong/text()').extract()) > 0 else None
            #print author
            support_votes, unsupport_votes = \
                    pic_section.xpath('.//a[contains(.,"oo")]/following-sibling::span/text()')\
                    .extract()
            
            #print support_votes + ':' + unsupport_votes
            pics = []
            for pic in pic_section.xpath('.//img'):
                pic_url = pic.xpath('./@src').extract()
                pic_ori_url = pic.xpath('./@org_src').extract()
                if len(pic_ori_url):
                    pics.append(pic_ori_url[0])
                elif len(pic_url):
                    pics.append(pic_url[0])
                else :
                    continue
            #print pics
            jdan_item = JdanScrapyItem()
            jdan_item['author'] = author
            jdan_item['support_votes'] = support_votes
            jdan_item['unsupport_votes'] = unsupport_votes
            jdan_item['image_urls'] = pics

        self.page_crawled += 1

        yield jdan_item

        yield scrapy.Request(next_page,self.parse)

    def close(self, reason):
        
        print reason

        print "page total:" + str(self.page_crawled)
