from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class Flipkart(CrawlSpider):
	name = "landmarkonnet"
	allowed_domains = ["www.landmarkonthenet.com"]
	start_urls = [
		"http://www.landmarkonthenet.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'landmarkonnet'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='primary']/div[@class='title']/h1/text()").extract()[0]
			#name: Integer
			item['price']=hxs.select("//div[@class='price']/p[@class='value']/span[@class='old-price']/text()").extract()
		except:
			toyield=0
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@id='thumbnailwrapper']/a[@class='imagemain ready']/img/@src").extract()
		except:
			item['images']=''
		try:
			item['details']=hxs.select("//div[@id='full-product-info']/div[@class='synopsis']/p[2]").extract()
		except:
			item['details']=[]
		try:
			#name: Integer
			item['shippingCost'] = hxs.select("//div[@class='price']/p[@class='value']/span[@class='current-price']").extact()
		except:
			item['shippingCost']=0
		try:
			#name: String
			item['delivery days']=hxs.select("//div[@class='purchase clearfix']/div[@class='stock']/p[@class='despatch-time']").extract()
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['publisher']=hxs.select("//div[@class='extended-details']/ul[@class='blank']/li[2]/text()").extract()[0]
		except:
			item['publisher']=''
		try:
			#name:Integer
			item['upc'] = hxs.select("//div[@class='extended-details']/ul[@class='blank']/li[5]").extract()[0]
		except:
			item['upc']=0
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='purchase clearfix']/div[@class='price']/p[@class='saving']/text()").extract()
		except:
			item['discount']=''
		
		if toyield:
		
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
		sleep(2)
