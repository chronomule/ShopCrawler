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
	name = "infibeam"
	allowed_domains = ["www.infibeam.com"]
	start_urls = [
		"http://www.infibeam.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'infibeam'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@id='ib_details']/h1[@class='fn']/text()").extract()[0]
			#name: Integer
			item['price']=hxs.select("//div[@id='priceDiv']/span[@class='linethrough']/span[@class='msrp']/text()").extract()
		except:
			toyield=0
		try:	
			#name: String
			item['warrenty']=hxs.select("//div[@id='specifications']/table[@class='fk-specs-type2'][11]/tbody/text()").extract()
		except:
			item['warrenty']=[]
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@id='ib_img_viewer']/ul/li/img[@id='imgMain']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			item['details']=hxs.select("//div[@id='ib_products']/p[2]/text()").extract()
		except:
			item['details']=[]
		try:
			#name: String
			item['deliveryDays'] = hxs.select("//div[@id='ib_details']/b/text()").extract()
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['warrenty'] = hxs.select("//div/span[@class='codSpan']/a[2]/img/@src").extract()
		except:
			item['warrenty']=''	
		try:
			#name: String
			item['shippingCost'] = hxs.select("//div[@id='priceDiv']//span[@class='infiPrice amount price']").extact()
		except:
			item['shippingCost']=0
		try:
			#name: String
			item['availability'] = hxs.select("//div[@id='colors']/span[@class='status']").extact()
		except:
			item['availability']=-1
		
		try:
			#name: String
			item['delivery days']=hxs.select("//div[@class='shipping-details']").extract()
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['publisher']=hxs.select("//div[@id='ib_products']/table//tr[2]/td[2]/text()").extract()[0]
		except:
			item['publisher']=''
		try:
			#name:Integer
			item['upc'] = hxs.select("//div[@id='ib_products']/table/tbody/tr[5]/td[2]/h2[@class='simple']").extract()[0]
		except:
			item['upc']=0
		try:
			#name: String
			item['discount']=hxs.select("//div[@id='ib_details']/div[@id='priceDiv']/span[6]").extract()
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
		