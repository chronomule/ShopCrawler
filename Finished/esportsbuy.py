from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import hashlib
import re
class FlipKart(CrawlSpider):
	name = "esportsbuy"
	allowed_domains = ["www.esportsbuy.com"]
	start_urls = [
		"http://www.esportsbuy.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'esportsbuy'
		toyield=1		##########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@id='pb-right-column']/h1").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//span[@id='old_price_display']/text()").extract()[0]
		except:
			toyield=0	
			item['images'] = ''
			
			item['details'] =  ''
		try:
			#name: String
			item['category'] = hxs.select("//div[@class='breadcrumb']/span[@class='navigation_end']/a/text()").extract()
		except:
			item['category']=''
		try:
			#name: String
			item['deliveryDays'] = hxs.select("//div[@id='pdt_ship_details']/div[3]/span/text()").extract()[1]
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['discount']=hxs.select("//div[@id='pdt_price_details']/div[@id='dicsount_lab_amt']/span[@id='reduction_amount_display']/text()").extract()
		except:
			item['discount']=''
		try:
			#name: String
			item['shippingCost'] = hxs.select("//div[@id='new_price']/span[@id='our_price_display']/text()").extract()[1]
		except:
			item['shippingCost']=''	
		try:
			#name: String
			item['availability']=hxs.select("//div[@id='avalibility_block']/span/text()").extract()
		except:
			item['availability'] = ''
		item['details'] = []
		item['upclist'] = []
		item['upc'] = ''
		item['publisher'] = ''
		item['discount'] = ''
		item['manufacturer'] = ''
		item['brand'] = ''
		item['warrenty'] = ''
		item['rating'] = ''
		item['upc'] = ''
		##########################################################################
		if toyield:
			item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
			item['deliveryDays']=re.sub('[^ a-zA-Z0-9]',' ',item['deliveryDays']).strip()
			item['warrenty']=re.sub('[^ a-zA-Z0-9]',' ',item['warrenty']).strip()
			item['shippingCost']=re.sub('[^ a-zA-Z0-9]',' ',item['shippingCost']).strip()
			item['brand']=re.sub('[^ a-zA-Z0-9]',' ',item['brand']).strip()
			item['manufacturer']=re.sub('[^ a-zA-Z0-9]',' ',item['manufacturer']).strip()
			item['discount']=re.sub('[^ a-zA-Z0-9]',' ',item['discount']).strip()
			item['publisher']=re.sub('[^ a-zA-Z0-9]',' ',item['publisher']).strip()
			item['upclist']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['upclist'] ]
			item['details']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['details'] ]
			item['category']=[ re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['category']]
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
