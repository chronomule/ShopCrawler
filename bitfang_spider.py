from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class bitfang(CrawlSpider):
	name = "bitfang18"
	allowed_domains = ["http://bitfang.com"]
	start_urls = [
		"http://bitfang.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'http://bitfang.com'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='ProdDetailsRight']/div[@class='prodDetailsPname']/h1/text()").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//div[@class='prodDetailsC3']/div[2]/span[@class='price-txt']/text()").extract()[0]
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='ProdDetailsLeft']/div[@class='ProdDetailsLeftWrap'][2]/img[@class='prodDetailsProduct']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['brand'] = hxs.select("//div[@id='tabs_container']/div/div[@id='Div2']/table[@class='rowbg1']//tr[@class='whitebg'][1]/td[2]/text()").extract()[0]
		except:
			item['brand']=''
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
