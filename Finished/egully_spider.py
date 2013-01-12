from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class egully(CrawlSpider):
	name = "egully12"
	allowed_domains = ["http://www.egully.com","www.egully.com"]
	start_urls = [
		"http://www.egully.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'egully.com'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@id='LayoutColumn2']/div[@id='ProductDetails']/div[@class='BlockContent']/h1/text()").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//div[@class='DetailRow'][2]/div[@class='Value']/em[@class='ProductPrice VariationProductPrice']/h2/b/text()").extract()
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='ProductThumbImage']/a/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['availability'] = hxs.select("//div[@class='ProductDetailsGrid']/div[@class='DetailRow'][7]/div[@class='Value']/text()").extract()[0]
		except:
			item['availability']=''
		try:
			#name: String
			item['shippingCost'] = hxs.select("//div[@class='DetailRow'][2]/div[@class='Value']/em[@class='ProductPrice VariationProductPrice']/h2/b/text()").extract()[0]
		except:
			item['shippingCost']=''
		try:
			#name: String
			item['brand'] = hxs.select("//div[@class='DetailRow'][3]/text()").extract()[0]
		except:
			item['brand']=''
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='ProductDetailsGrid']/div[@class='DetailRow'][2]/div[@class='Value']/span[@class='YouSave']/text()").extract()[1]
		except:
			item['discount']=''
		try:
			#name: String
			item['details']=hxs.select("//div[@id='ProductDescription']/div[@class='ProductDescriptionContainer']/div[@class='line description item_desc_text'][3]/text()").extract()[0]
		except:
			item['details']=[]
		###########################################################################
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
