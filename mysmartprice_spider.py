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
    name = "mysmartprice"
    allowed_domains = ["mysmartprice.com"]
    start_urls = [
        "http://www.mysmartprice.com/mobile/nokia-n8-msp426",
		"http://www.mysmartprice.com/camera/sigma-70-300mm-f4-5.6-apo-dg-macro-lens-motorized-for-sony-dslr-msf31036",
		"http://www.mysmartprice.com/computer/acer-aspire-4750z-mslap200002"
    ]
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@class='pt_row']")
        items = []
        productname = hxs.select("//div[@class='item_title']/h2/text()").extract()
        brandname,rawdetails,imagelink = '','',''
        try:
			brandname= hxs.select("//div[@class='pt_meta_topunit']/div[@class='alignleft']").extract()[0].split('&gt;')[1]
        except:
			print "Unexpected error:"
        try:
			rawdetails = hxs.select("//div[@class='detail_text']/p").extract()
        except:
			print "Unexpected error:"
        try:
			imagelink=hxs.select("//div[@class='pt_meta_head']//img/@src").extract()[0]
        except:
			print "Unexpected error:"
        for site in sites:
          item = MySmartPrice()
          item['name'] = productname
          item['rating'] = 0
          item['brand'] = brandname
          item['manufacturer'] = brandname
          try:
			item['url'] = site.select("table/tr[1]/td[5]/a/@href").extract()[0]
          except:
			print "Unexpected error:"
          try:
			item['deliveryDays'] = site.select('table/tr[1]/td[3]/text()').extract()[0]
          except:
			print "Unexpected error:"
          try:
			item['siteName'] = site.select('table/tr/td[1]/a/img/@alt').extract()[0]
          except:
			print "Unexpected error:"
          try:
			item['price'] = site.select('table/tr/td[2]/b/text()').extract()[0]
          except:
			print "Unexpected error:"
          try:
			item['shippingCost'] = site.select('table/tr[1]/td[4]/text()').extract()[0]
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
    