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
	allowed_domains = ["http://www.naaptol.com","naaptol.com"]
	start_urls = [
		"http://www.naaptol.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'naaptol.com'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='prodPromDesDiv'][1]/div[@class='prodTitle']/h1").extract()
			#name: String
			item['price'] = hxs.select("//div[@class='priceDiv']/p[@class='mrpPrice']/span[@class='lineThro']/text()").extract()
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='prodPromImgClm']/div[@id='prodImgLayout']/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: Float
			item['rating'] = hxs.select("//div[@class='prodPromDesLayout']/div[@class='prodPromDesDiv'][2]").extract()
		except:
			item['rating']=-1
		try:
			#name: StringList
			item['details']=hxs.select("//div[@class='prodPromDesLayout']/p[@class='prodDes']/text()").extract()[0]
		except:
			item['details']=[]
		try:
			#name: String
			item['shippingCost']=hxs.select("//div[@class='prodPromDesDiv'][3]/div[@class='priceDiv']/h2/text()").extract()[0]
		except:
			item['shippingCost']=[]
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='prodPromDesDiv'][3]/div[@class='priceDiv']/h2/text()").extract()[0]
		except:
			item['discount']=[]
		try:
			#name: String
			item['upc']=hxs.select("//div[@class='prodPromDesLayout']/div[3]/p/text()").extract()[0]
		except:
			item['upc']=''
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
