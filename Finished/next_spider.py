from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import hashlib
import re
class Next(CrawlSpider):
	name = "next"
	allowed_domains = ["www.next.co.in","next.com"]
	start_urls = [
		"http://www.next.co.in"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'next.co.in'
		toyield=1
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='ctl_aboutbrand']/h1/text()").extract()[0]
			#name: Integer	
			item['price']=hxs.select("//div[@class='productprices']").extract()	
		except:		
			toyield=0
		try:
			#name: StringList		
			item['images'] = hxs.select("//img[@id='bankImage']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String	
			item['shippingCost']=hxs.select("//span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_lblOfferPrice']/text()").extract()
		except:
			item['shippingCost'] = ''
		try:
			#name: String
			item['brand']=hxs.select("//div[@class='productbrand']/span[@class='brandlname']/text()").extract()
		except:
			item['brand']=''
		try:
			#name: String
			item['deliveryDays']=hxs.select("//div[@class='leftpane']/img/@src").extract()
		except:
			item['deliveryDays']=''
		try:
			#name: StringList
			item['details']=hxs.select("//div[@class='ctl_aboutproduct']/p[@class='product_desc']/text()").extract()
		except:
			item['details']=[]
		item['availability'] = -1
		item['manufacturer'] = ''
		item['upc'] = ''
		item['upclist'] = ''
		try:
			#name: Float
			item['rating']=hxs.select("//div[@id='ctl00_ContentPlaceHolder1_Ratings_ctl00_divAvgRat']").extract()
		except:
			item['rating']=-1
		if toyield:
			item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
			#item['deliveryDays']=re.sub('[^ a-zA-Z0-9]',' ',item['deliveryDays']).strip()
			#item['warrenty']=re.sub('[^ a-zA-Z0-9]',' ',item['warrenty']).strip()
			#item['shippingCost']=re.sub('[^ a-zA-Z0-9]',' ',item['shippingCost']).strip()
			#item['brand']=re.sub('[^ a-zA-Z0-9]',' ',item['brand']).strip()
			#item['manufacturer']=re.sub('[^ a-zA-Z0-9]',' ',item['manufacturer']).strip()
			#item['discount']=re.sub('[^ a-zA-Z0-9]',' ',item['discount']).strip()
			#item['publisher']=re.sub('[^ a-zA-Z0-9]',' ',item['publisher']).strip()
			#item['upclist']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['upclist'] ]
			#item['details']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['details'] ]
			#item['category']=[ re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['category']]
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
