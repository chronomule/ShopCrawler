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
	name = "myntra"
	allowed_domains = ["www.myntra.com"]
	start_urls = [
		"http://www.myntra.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'myntra'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='product-detail-block-left left']/h1[@class='product-title']/text()").extract()[0]
			#name: Integer
			item['price']=hxs.select("//div[@class='pricing-info mt10']/span[@class='oprice strike']/text()").extract()
		except:
			toyield=0
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@id='area_default']/a[@id='thumb_0']/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['details']=hxs.select("//div[@class='product-detail-block last right']/div[@class='clear']/div[@class='product-description']/p/text()").extract()
		except:
			item['details']=''
		try:
			#name: Integer
			item['shippingCost'] = hxs.select("//div[@class='pricing-info mt10']/span[@class='dprice']/text()").extract()
		except:
			item['shippingCost']=0
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='pdp-discount-align pdp-sploff pdp-trigger']/b/text()").extract()
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