from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class Flipkart(CrawlSpider):
	name = "babyoye"
	allowed_domains = ["www.babyoye.com"]
	start_urls = [
		"http://www.babyoye.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'babyoye'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='prodCont']/form[@id='product_addtocart_form']/div[@class='head clearfix']/h1/text()").extract()[0]
			#name: StringList
			item['price']=hxs.select("//div[@id='t_price']/div[@class='totalPrice']/text()").extract()
		except:
			toyield=0
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@class='zoomCont']/a[@id='MagicZoomImagemagictoolbox1']/img[@id='zoomerImg']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['details']=hxs.select("//div[@class='proDescript']/text()").extract()
		except:
			item['details']=''
		#try:
		#	#name: Integer
		#	item['shippingCost'] = hxs.select("//div[@class='pricing-info mt10']/span[@class='dprice']/text()").extract()
		#except:
		#	item['shippingCost']=0
		try:
			#name: String
			item['availability']=hxs.select("//div[@class='detBox']/p[2]/span[@class='green']/text()").extract()
		except:
			item['availability']=''
		try:		
			#name: String
			item['upc']=hxs.select("//div[@class='head clearfix']/img[@class='code']/@src").extract()
		except:
			item['upc']=''
		try:
			#name: Integer
			item['rating']=hxs.select("//div[@class='ratingBox mt5']/div[@id='rate1']/div[@class='star  star-left on']").extract()
		except:
			item['rating']=''
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