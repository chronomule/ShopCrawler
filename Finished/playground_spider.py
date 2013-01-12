from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class letsbuy(CrawlSpider):
	name = "playground"
	allowed_domains = ["www.playgroundonline.com"]
	start_urls = [
		"http://www.playground.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'letsbuy'
		toyield=1
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='pageHeader']/div[@class='catName']/text()").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//div[@class='right'][3]/span[@class='skuOurPrice r11b']").extract()[0]
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='detImage'][1]/a[@id='bpic']/img[@id='bigpic']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: StringList
			item['details'] =  hxs.select("//div[@class='detRight']/table//tr[1]/td/div[@class='detRightRow'][1]/text()").extract()
		except:
			item['details']=[]
		try:
			#name: String
			item['deliveryDays'] = hxs.select("//div[@class='detPriceArea']/div[@class='right'][4]/text()").extract()
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['upc'] = hxs.select("//div[@class='detPriceArea']/div[@class='right'][1]/span[@class='skuOurPrice']").extract()
		except:
			item['upc']=''
		item['upclist'] = ''
			
		if toyield:
			item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
			#item['deliveryDays']=re.sub('[^ a-zA-Z0-9]',' ',item['deliveryDays']).strip()
			
			#item['shippingCost']=re.sub('[^ a-zA-Z0-9]',' ',item['shippingCost']).strip()
			
			#item['discount']=re.sub('[^ a-zA-Z0-9]',' ',item['discount']).strip()
			#item['publisher']=re.sub('[^ a-zA-Z0-9]',' ',item['publisher']).strip()
			
			item['details']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['details'] ]
			#item['category']=[ re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['category']]
		yield item
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(self.start_urls[0]+url,callback=self.parse)
			except:
				print "Item Unexpected error:"
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(url, callback=self.parse)
			except:
				print  "Unexpected error:"
		sleep(2)
