from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import hashlib
import re
class watch(CrawlSpider):
	name = "watchkart"
	allowed_domains = ["www.watchkart.com","watchkart.com"]
	start_urls = [
		"http://www.watchkart.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'watchkart'
		toyield=1	##########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='right-product']/span[@class='product-name']").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//span[@class='second-bl']//span[@class='reg-price']").extract()[0]
			
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='MagicThumb-expanded']/div[1]/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['shippingCost'] = hxs.select("//span[@class='spcl-price']").extract()
		except:
			item['shippingCost']=''
		try:
			#name: String
			item['discount']=hxs.select("//span[@class='you-save']/span").extract()
		except:
			item['discount']=''
		try:
			#name: StringList
			item['details']=hxs.select("//div[@class='info-tab-right']").extract()
		except:
			item['details'] = ''
		try:
			#name: String
			item['deliveryDays']=hxs.select("//div[@class='add-to-cart-butt']/span[@class='bot-text']").extract()
		except:
			item['deliveryDays'] =''
		try:
			#name: String
			item['brand']=hxs.select("//div[@class='collateral-box attribute-specs']/div[@class='info-tab-left']/table[@id='product-attribute-specs-table']//tr[@class='odd'][2]/td[@class='data last']").extract()[0]
		except:
			item['brand'] = ''
		try:
			#name: String
			item['manufacturer']=hxs.select("//tr[@class='odd']/td[@class='data last']").extract()
		except:
			item['manufacturer'] = ''
		item['warrenty'] = ''
		item['rating'] = ''
		item['availability'] = ''
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
