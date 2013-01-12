from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class futureBazaar(CrawlSpider):
	name = "futurebazaar"
	allowed_domains = ["www.futurebazaar.com","futurebazaar.com"]
	start_urls = [
		"http://www.futurebazaar.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'futurebazaar.com'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@id='product_desc']/h1/text()").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//td[@class='price_value']/span[@class='fs']/text()").extract()[0]
		except:
			toyield=1
			item['price']
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='prod_img_link']/a[@id='product_zoom_image']/img[@id='display_img']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['deliveryDays'] =hxs.select("//div[@class='pdp_add_qty']/table[@class='pdp_price']//tr[3]/td[@class='price_value pad0']/span/span[@class='f333']").extract()[0]
		except:
			item['deliveryDays']=''
		try:
			#name: Integer
			item['availability'] = hxs.select("//table[@class='pdp_price']//tr[2]/td[@class='price_value']/span/span[@class='fgreen fb']").extract()
		except:
			item['availability']=-1
		try:
			#name: String
			item['shippingCost'] = hxs.select("//td[@class='price_value fcop fb f17']").extract()[0]
		except:
			item['shippingCost']=''
		try:
			#name: String
			item['brand'] = hxs.select("//div[@class='marb5 brand_row f11 mart5']").extract()[0]
		except:
			item['brand']=''
		try:
			#name: Float
			item['rating'] = hxs.select("//div[@class='marb10 ratings_row f11 ']/div[@class='left'][1]/text()").extract()[0]
		except:
			item['rating']=-1
		try:
			#name: String
			item['discount']=hxs.select("//table[@class='pdp_price mart10 marb10']//tr[3]/td[@class='price_value']").extract()[0]
		except:
			item['discount']=''
		try:
			#name: String
			item['publisher']=hxs.select("//table[@class='pdp_price mart10 marb10']//tr[3]/td[@class='price_value']").extract()[0]
		except:
			item['publisher']=''
		try:
			#name: String
			item['upclist']=[]
		except:
			item['upclist']=[]
		try:
			#name: String
			item['category']=[]
		except:
			item['category']=[]
		try:
			#name: String
			item['warrenty']=''
		except:
			item['warrenty']=''
		try:
			#name: StringList
			item['details']=hxs.select("//div[@class='pdp_tab1_desc marb10']/text()").extract()
		except:
			item['details']=[]
		###########################################################################
		if toyield:
			item['price'] = re.sub('\D','',re.sub('\.00','',item['price']))
			item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
			item['deliveryDays']=re.sub('[^ a-zA-Z0-9]',' ',item['deliveryDays']).strip()
			item['warrenty']=re.sub('[^ a-zA-Z0-9]',' ',item['warrenty']).strip()
			item['shippingCost']=re.sub('[^ a-zA-Z0-9]',' ',item['shippingCost']).strip()
			item['brand']=re.sub('[^ a-zA-Z0-9]',' ',item['brand']).strip()
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
