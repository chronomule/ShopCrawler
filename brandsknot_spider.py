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
	name = "brandsknot"
	allowed_domains = ["http://www.brandsknot.com","www.brandsknot.com"]
	start_urls = [
		"http://www.brandsknot.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'brandsknot'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//td[@class='white_16']/table//tr/td[1]/text()").extract()[0]
			#name: Integer
			#item['price'] = hxs.select("//td[@class='white_16'][2]/input[@id='txtprice']/text()").extract()[2]
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//img[@id='imges']/@src").extract()[0]
		except:
			item['images']=['wrong']
		
		###########################################################################
		if toyield:
			#item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
			
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