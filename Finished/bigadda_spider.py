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
	name = "bigadda"
	allowed_domains = ["www.bigadda.com"]
	start_urls = [
		"http://www.bigadda.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'bigadda'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='product-shop']/div[@class='product-name']/h1/text()").extract()
			#name: String
			item['price']=hxs.select("//div[@class='price-box']/div[@class='price-txt']/p[@class='our-price']/span[@class='price']/text()").extract()[0]
		except:
			toyield=0
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@id='id_20023']/a/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['warrenty'] = hxs.select("//div[@class='product-essential']/form[@id='product_addtocart_form']/div[@class='product-shop']/div[@class='warranty-box']/text()").extract()
		except:
			item['warrenty']=[]
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='product-shop']/div[@class='price-box']/div[@class='percent-off']/div[@class='percent-off iconsprite']/text()").extract()[0]
		except:
			item['discount']=''
		try:
			#name: String
			item['brand']=hxs.select("//tr[@class='even'][1]/text()").extract()[0]
		except:
			item['brand']=''
		try:
			#name: String
			item['upc'] = hxs.select("//tr[@class='first odd']/text()").extract()[0]
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
		