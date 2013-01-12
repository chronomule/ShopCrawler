from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class indiaplaza(CrawlSpider):
	name = "indiaplaza"
	allowed_domains = ["www.indiaplaza.com","indiaplaza.com"]
	start_urls = [
		"http://www.indiaplaza.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['url'] = response.url
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'indiaplaza'
		toyield=1
		##########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='fdpSkuArea']//h1/text()").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//div[@class='priceArea']/div[@class='fdpOurPrice']/span[@class='blueFont']/text()").extract()
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='skuCol']/img[@id='imgpfd']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: StringList
			item['details'] =  hxs.select("//div[@class='inContent']/p[1]/text()").extract()
		except:
			item['details']=[]
		try:
			#name: String
			item['deliveryDays'] = hxs.select("//div[@class='fdpNormShip padt12']/span[@class='delDateQuest']/text()").extract()[0]
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='fdpSave']/text()").extract()[0]
		except:
			item['discount']=''
		try:
			#name: String
			item['warrenty'] = hxs.select("//div[@class='sub_list']//li[3]/text()").extract()[0]
		except:
			item['warrenty']=''
		try:
			#name: String
			item['shippingCost'] = hxs.select("//div[@class='priceArea']/div[@class='fdpOurPrice']/span[@class='blueFont'][1]/text()").extract()[0]
		except:
			item['shippingCost']=''
		try:
			#name: Float
			item['rating'] = hxs.select("//div[@class='ratingstar rstar37']").extract()
		except:
			item['rating']=-1
		try:
			#name: String
			item['brand']= hxs.select("//div[@class='specColr'][1]/div[@class='specMidLine']/div[@class='fdpSpecCol2r'][1]/text()").extract()[0]
		except:
			item['brand'] = ''
		try:
			#name: String
			item['publisher']= hxs.select("//div[@class='bksfdpltrArea']/ul/li[1]/span[@class='greyFont']/text()").extract()[0]
		except:
			item['publisher']=''
		try:
			#name: String
			item['upc'] = hxs.select("//div[@class='bksfdpltrArea']/ul/li[2]/span[@class='greyFont']/h2").extract()
		except:
			item['upc']=''
		try:
			#name: String
			item['category'] = []
		except:
			item['category']=[]
		item['manufacturer'] = ''
		item['availability'] = ''
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



	
