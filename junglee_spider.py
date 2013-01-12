from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import MySmartPrice 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class MySmartPriceSpider(CrawlSpider):
    name = "junglee"
    allowed_domains = ["www.junglee.com"]
    start_urls = [
        "http://www.junglee.com"
    ]
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//table[@class='outdent']//tr[1]")
        items = []
        productname = hxs.select("//div[@id='productAttributes_10000']/h1/text()").extract()[0]
        rawdetails,imagelink = '',''
        try:
			rawdetails = hxs.select("//div[@class='displayBlock'][1]/div[@class='descriptionContent']/text()").extract()
        except:
			print "Unexpected error:"
        try:
			imagelink=hxs.select("//div[@id='mainImage']/a/img/@src").extract()[0]
        except:
			print "Unexpected error:"
        for site in sites:
          item = MySmartPrice()
          item['name'] = productname
          try:
			item['url'] = site.select("//table[@class='outdent']//tr[1]/td[@class='merchant-info']//a/@href").extract()[0]
          except:
			print "Unexpected error:"
          try:
			item['deliveryDays'] = site.select("//table[@class='outdent']//tr[1]/td[@class='offer-delivery-time']").extract()
          except:
			print "Unexpected error:"
          try:
			item['siteName'] = site.select("//table[@class='outdent']//td[@class='merchant-info']//a/@href").extract()[0]
          except:
			print "Unexpected error:"
          try:
			item['price'] = site.select("//div[@id='priceContainer']/div[@class='advPriceContainer priceContainer']/div[2]/span[@id='advPrice']/text()").extract()[0]
          except:
			print "Unexpected error:"
          item['sourceLink'] = response.url
          item['details'] = rawdetails
          item['identifier'] = response.url+":"+item['siteName']
          item['images'] = imagelink
          items.append(item)
        sleep(2)
        for item in items:
           yield item
        for url in hxs.select('//a/@href').extract():
           try:
              yield Request(self.start_urls[0]+url, callback=self.parse)
           except:
              print  "Unexpected error:"
        for url in hxs.select('//a/@href').extract():
           try:
              yield Request(url, callback=self.parse)
           except:
              print  "Unexpected error:"