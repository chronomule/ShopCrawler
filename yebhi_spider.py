from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class YeBhiSpider(CrawlSpider):
	name = "YeBhiSpider"
	allowed_domains = ["yebhi.com"]
	start_urls = [
		"http://www.yebhi.com/117140/PD/Canon-Point-and-Shoot-Camera-Powershot-A3400-IS-Silver.htm"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'yebhi'
		toyield=1
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='product-desc']/text()").extract()[0]
			#name: Integer
			item['price'] = int(re.sub('\D','',re.sub('\.00','',hxs.select("//span[@class='price-offer']").extract()[0])))
		except:
			toyield=0
		try:
			#name: StringList
			item['images']=hxs.select("//img[@id='ctl00_ContentPlaceHolderMain_productView1_usrprodimage_myimage2']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: Integer
			item['availability']= str(re.sub('[^ a-zA-Z0-9]','',hxs.select("//div[@class='product-instock']/text()").extract()[0]))
		except:
			item['availability']= -1
		try:
			#name: String
			item['brand']=hxs.select("//div[@class='middle-content-bg']/div[2]/div[1]/a/img/@src").extract()
		except:
			item['brand']=' '
		try:
			#name: String
			item['upc']=hxs.select("//div[@class='middle-content-bg']/div[2]/div[1]/div[@class='product-code']/text()").extract()
		except:
			item['upc']=''
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