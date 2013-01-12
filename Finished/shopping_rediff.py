from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import hashlib
import re
class rediff_shopping(CrawlSpider):
	name = "shopping_rediff"
	allowed_domains = ["www.shopping.rediff.com","shopping.rediff.com","books.rediff.com"]
	start_urls = [
		"http://www.shopping.rediff.com","shopping.rediff.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'Rediff'
		toyield=1			##########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//input[@name='prtitle']/@value").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//div[@class='floatL']/table//tr/td/table//tr[2]/td[5]/table//tr[1]/td/table//tr/td[@class='sb13']/font[1]/b/text()").extract()
		except:
			toyield=0
		try:
			#name: StringList	
			item['images'] = hxs.select("//div[@class='floatL']/table//tr/td/table//tr[2]/td[2]/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: StringList
			item['details'] =  hxs.select("//div[@class='floatL width100per mar5']/div[@class='padding10']/text()").extract()
		except:
			item['details']=[]
		try:
			#name: String
			item['deliverydays']=hxs.select("//td[@class='sb13']/text()").extract()[0]
		except:
			item['deliveryDays'] = ''
		try:
			#name: String
			item['warrenty']=hxs.select("//div[@class='pg']/div[@class='sp'][5]/div[@class='rt']/text()").extract()
		except:
			item['warrenty'] = ''
		try:
			#name: String
			item['publisher']=hxs.select("//div[@class='floatL']/table//tr/td/table//tr[2]/td[3]/table//tr[3]/td/text()").extract()
		except:
			item['publisher']=''
		try:
			#name: String
			item['upc']=hxs.select("//div[@class='floatL']/table//tr/td/table//tr[2]/td[3]/table//tr[5]/td/text()").extract()[0]#UPC/ISBN how to get the ISBN
		except:
			item['upc'] = ''
		##########################################################################
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
