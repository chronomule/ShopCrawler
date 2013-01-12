from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class sulekha(CrawlSpider):
	name = "sulekha"
	allowed_domains = ["www.sulekha.com","mobiles.sulekha.com"]
	start_urls = [
		"http://www.sulekha.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'sulekha.com'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='floatbugfix']/h2[@class='subhead']/text()").extract()[0]
			#name: Integer
			item['price']=hxs.select("//div[@class='floatbugfix']/ul[@class='speclist floatbugfix']/li[5]/text()").extract()[0]
		except:
			toyield=1
		try:	
			#name: String
			item['warrenty']=hxs.select("//div[@id='specifications']/table[@class='fk-specs-type2'][11]/tbody/text()").extract()
		except:
			item['warrenty']=[]
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@class='bd']/div[@class='flushleft']/a/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['warrenty'] = hxs.select("//div/span[@class='codSpan']/a[2]/img/@src").extract()
		except:
			item['warrenty']=''	
		try:
			#name: String
			item['shippingCost'] = hxs.select("//div[@class='mobile-deals-value']/b[@class='mobbltpd ftlt']/span[4]/text()").extact()
		except:
			item['shippingCost']=0
		try:
			#name: String
			item['availability'] = hxs.select("//div[@id='colors']/span[@class='status']").extact()
		except:
			item['availability']=-1
		try:
			#name:Integer
			item['upc'] = hxs.select("//div[@id='ib_products']/table/tbody/tr[5]/td[2]/h2[@class='simple']").extract()[0]
		except:
			item['upc']=0
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='mobile-deals-offer']/text()").extract()
		except:
			item['discount']=''
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
		