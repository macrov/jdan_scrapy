# -*- coding: utf-8 -*-
import scrapy
from jdan_scrapy.items import JdanScrapyItem


class JdanpicSpider(scrapy.Spider):
    name = "jdanpic"
    allowed_domains = ["jandan.net"]
    start_urls = (
        'http://www.jandan.net/pic',
    )
    page_crawled = 0

    def parse(self, response):

        next_page = response.xpath(
                '//span[@class="current-comment-page"]/following-sibling::*[1]')[0]\
                        .xpath('@href').extract()[0]


        for pic_section in response.xpath('//ol[@class="commentlist"]/li'):
            print pic_section.extract()
            flag = pic_section.xpath('.//div[@class="author"]')
            print flag
            if len(flag) == 0:
                continue
            author = pic_section.xpath('.//strong/text()').extract()[0] if len(pic_section.xpath('.//strong/text()').extract()) > 0 else None
            print author
            support_votes, unsupport_votes = \
                    pic_section.xpath('.//a[contains(.,"oo")]/following-sibling::span/text()')\
                    .extract()
            
            print support_votes + ':' + unsupport_votes
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
            print pics
            jdan_item = JdanScrapyItem()
            jdan_item['author'] = author
            jdan_item['support_votes'] = support_votes
            jdan_item['unsupport_votes'] = unsupport_votes
            jdan_item['pics'] = pics

        self.page_crawled += 1

        yield jdan_item

        yield scrapy.Request(next_page,self.parse)

    def close(self, reason):
        
        print reason

        print "page total:" + str(self.page_crawled)
