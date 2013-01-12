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
	name = "junglee"
	allowed_domains = ["www.junglee.com"]
	start_urls = [
		"http://www.junglee.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'junglee'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@id='productAttributes_10000']/h1[@class='productTitle']/text()").extract()
			#name: String
			item['price']=hxs.select("//div[@class='advPriceContainer priceContainer']/div[2]/span[@id='advPrice']/text()").extract()
		except:
			toyield=0
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@id='mainImageContainer']/div[@id='mainImage']/a/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['manufacturer'] = hxs.select("//div[@id='center-8']/div[@class='shortDescriptionContainer']/div[@class='shortProductDescription']/table//tr[1]/td[@class='featureValue']/text()").extract()[0]
		except:
			item['manufacturer']=[]
		try:
			#name: String
			item['deliveryDays']=hxs.select("//div[@class='offers-international']/table[@class='outdent']/[@class='offer-has-map offer-hidden-map']/tr[1]/td[@class='offer-delivery-time']/ol[@class='offer-delivery-info']/li/text()").extract()[0]
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['rating']=hxs.select("//div[@class='shortProductDescription']/table//tr[@id='jungleeAGRating']/td[@class='featureValue']/text()").extract()[0]
		except:
			item['rating']=''
		try:
			#name: String
			item['brand']=hxs.select("//div[@id='productDescription']/table[1]//tr[2]/td[@class='featureValue']/text()").extract()[0]
		except:
			item['brand']=''
		try:
			#name: String
			item['upc'] = hxs.select("//div[@id='productDescription']/table[1]//tr[3]/td[@class='featureValue']/text()").extract()[0]
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
		