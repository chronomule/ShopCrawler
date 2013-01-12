from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import hashlib
import re
class Healthkart(CrawlSpider):
	name = "healthkart"
	allowed_domains = ["www.healthkart.com"]
	start_urls = [
		"http://www.healthkart.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName']='healthkart'
		toyield=1
		##########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='product_details']/h2[@class='prod_title']").extract()[0]
			item['price'] = hxs.select("//div[@class='prices']/div[@class='hk']/span[@class='num']/text()").extract()[0]
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='zoomPad']/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: StringList
			item['details'] = hxs.select("//div[@class='product_details']/div[@class='pbox1']/p/text()").extract()
		except:
			item['details']=[]
		try:
			#name: String
			item['deliveryDays']=hxs.select("//div[@class='infos']/span[@class='info orange']/text()").extract()
		except:
			item['deliveryDays'] =''
		try:
			#name: String
			item['shippingCost'] = hxs.select("//div[@class='prices']/div[@class='hk']/span[@class='num']/text()").extract()
		except:
			item['shippingcost']=''
		item['rating'] = ''
		item['availability'] = ''
		try:
			item['brand']=hxs.select("//div[@class='infos']/span[@class='info']/a[@class='bl']/text()").extract()
		except:	
			item['brand'] = ''
		item['manufacturer'] = ''
		item['warrenty'] = ''
		item['upc'] = ''
		item['upclist'] = ''
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
	