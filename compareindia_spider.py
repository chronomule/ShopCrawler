from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class homeshop18(CrawlSpider):
	name = "compareindia"
	allowed_domains = ["http://www.compareindia.in.com","compareindia.in.com"]
	start_urls = [
		"http://www.compareindia.in.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'compareindia.in.com'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@id='prod0']/a/img[@id='img_product_com']/@src").extract()
			#name: String
			item['price'] = hxs.select("//div[@id='tool_tip']/span[@id='productPrice']/strong/span[@id='productD_price269082']/text()").extract()
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@id='prod1']/a/img[@id='img_product_com']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: Float
			item['rating'] = hxs.select("//div[@class='FL brgt PT15']/div[@class='clearfix']").extract()
		except:
			item['rating']=-1
		try:
			#name: StringList
			item['details']=hxs.select("//div[@class='cumcolL']/div[@class='MT20'][1]/div[@class='bl_14n']/div[@id='stdesc']/text()").extract()[0]
		except:
			item['details']=[]
		###########################################################################
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
