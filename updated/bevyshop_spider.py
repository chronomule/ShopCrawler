from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData
from time import sleep 
import re
import hashlib
class PriceDekho(CrawlSpider):
    name = "bevyshop"
    allowed_domains = ["bevyshop.com"]
    start_urls = [
        "http://www.bevyshop.com"
    ]
    def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'bevyshop.com'
		toyield = True
		try:
			item['name'] = hxs.select("//div[@class='center']/h1/text()").extract()[0]
			item['price'] = int(re.sub('\D','',re.sub('\.00','',hxs.select("//td[2]/span[@class='main_price']").extract()[0])))
		except:
			toyield=False
		try:
			item['brand'] = hxs.select("//td[2]/a/text()").extract()[0]
		except:
			item['brand']=''
		try:
			item['availability'] = hxs.select("//tr[2]/td[2]/text()").extract()[0]
		except:
			item['availability']=''
		try:
			item['model'] = hxs.select("//tr[3]/td[2]/text()").extract()[0]
		except:
			item['model']=''
		try:
			item['category'] = re.sub('\D','',re.sub('\.00','',hxs.select("//div[@id='breadcrumb']/text()").extract()))
		except:
			item['category']=[]
		
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