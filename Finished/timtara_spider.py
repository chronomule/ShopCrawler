from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class homeshop18(CrawlSpider):
	name = "timtara"
	allowed_domains = ["http://www.timtara.com","www.timtara.com"]
	start_urls = [
		"http://www.timtara.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'timtara'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='textgray'][1]/span[@class='textblackbold']/text()").extract()[0]
			#name: Integer
			item['price'] = re.sub('\D','',re.sub('\.00','',hxs.select("//div[@class='DetailRow'][1]/div[@class='Value']/strike/text()").extract()[0].encode("utf-8",'ignore')))
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='ProductTinyImageList']/ul/li[@id='TinyImageBox_0']/div/a/img[@id='TinyImage_0']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['warrenty'] = hxs.select("//div[@class='ProductDetailsGrid textgray']/div[@class='DetailRow'][4]/div[@class='Value']/text()").extract()[0]
		except:
			item['warrenty']=''
		try:
			#name: String
			item['shippingCost'] = hxs.select("//div[@class='Value']/em[@class='ProductPrice VariationProductPrice']/b/text()").extract()[0]
		except:
			item['shippingCost']=''
		try:
			#name: String
			item['brand'] = hxs.select("//div[@class='ProductDetailsGrid textgray']/div[@class='DetailRow'][3]/div[@class='Value']/a/text()").extract()[0]
		except:
			item['brand']=''
		try:
			#name: String
			item['upc'] = hxs.select("//div[@class='ProductDetailsGrid textgray']/div[@class='DetailRow'][5]/div[@class='Value']/text()").extract()[0]
		except:
			item['upc']=0
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='ProductDetailsGrid ProductAddToCart']/div[2]/div[3]/div[@class='relativ'][1]/div[@class='buybiggray']/text()").extract()[0]
		except:
			item['discount']=''
		try:
			#name: String
			item['publisher']=hxs.select("//table[@class='productKeywords']/text()").extract()[0]
		except:
			item['publisher']=''
		
		###########################################################################
		if toyield:
			item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
			
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