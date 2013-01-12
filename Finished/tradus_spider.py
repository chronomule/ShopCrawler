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
	name = "tradus"
	allowed_domains = ["www.tradus.in"]
	start_urls = [
		"http://www.tradus.in"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'tradus'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@id='left-content-product-details-part1']/h1[@class='left-content-product-heading']/text()").extract()
			#name: String
			item['price']=hxs.select("//b[@id='tPrice']/text()").extract()[0]
		except:
			toyield=0
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@class='product_image_bg']/table//tr/td[1]/ul/li/a[@class='cloud-zoom-gallery']/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['shippingCost'] = hxs.select("//b[@id='tPrice']/text()").extract()
		except:
			item['shippingCost']=[]
		try:
			#name: Float
			item['rating']=hxs.select("//div[@id='seller_review_block']").extract()[0]
		except:
			item['rating']=''
		try:
			#name: String
			item['publisher']=hxs.select("//div[@id='product-specification']/table[5]//tr/td[@id='product-spec']/p/text()").extract()[0]
		except:
			item['publisher']=''
		try:
			#name: Integer
			item['upc'] = hxs.select("//div[@id='product-specification']/table[4]//tr/td[@id='product-spec']/p").extract()[0]
		except:
			item['upc']=0
		
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
		