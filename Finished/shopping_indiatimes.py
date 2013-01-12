from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import hashlib
import re
class ShoppingIndia(CrawlSpider):
	name = "shopping.indiatimes.com"
	allowed_domains = ["www.shopping.indiatimes.com","shopping.indiatimes.com"]
	start_urls = [
		"http://www.shopping.indiatimes.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'shopping.indiatimes.com'
		toyield=1
	##########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='producthead']/h1").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//div[@class='priceinfo flt']/div[@class='oldprice'][1]").extract()[0]
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='productimghigh']//img/@src").extract()
		except:
			item['images']=['wrong']

		try:
			#name: StringList		
			item['details'] =  hxs.select("//div[@class='productdetail']/p").extract()
		except:
			item['details']=[]
		try:
			#name: String
			item['deliveryDays'] = hxs.select("//div[@class='stockinfo']/span[@class='checkDelivery frt']/b[@class='checkDeliverysla']/text()").extract()[0]
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='oldprice'][2]/span[@class='price yoursaving']").extract()[2]
		except:
			item['discount']=''
		try:
			#name: String
			item['shippingCost'] = hxs.select("//div[@class='priceinfo flt']/div[@class='newprice']").extract()
		except:
			item['shippingCost']=''
		try:
			#name: String
			item['publisher']=hxs.select("//div[@class='floatL']/table//tr/td/table//tr[2]/td[3]/table//tr[3]/text()").extract()[3]
		except:
			item['publisher']=''	
		try:
			#name: Integer
			item['upc']=hxs.select("//div[@class='floatL']/table//tr/td/table//tr[2]/td[3]/table//tr[5]").extract()[5]
		except:
			item['upc']=0
		try:	
			#name: String
			item['brand']=hxs.select("//div[@class='productspecification']/table//tr[1]/td/strong/text()").extract()[1]
		except:
			item['brand'] = ''
		try:
			#name: String
			item['warrenty']=hxs.select("//div[@class='productspecification']/table//tr[3]/td/dl/dd/text()").extract()[0]
		except:
			item['warrenty'] = ''
		try:	
			#name: String
			item['rating']=hxs.select("//div[@class='rating flt']/span/span/text()").extract()[0]
		except:
			item['rating'] = ''
		try:
			#name: String
			item['availability']=hxs.select("//div[@class='stockinfo']/span[@class='instock flt']/text()").extract()[0]
		except:	
			item['availability'] = ''
		item['manufacturer'] = ''
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
