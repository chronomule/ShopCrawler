from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import MetaSitesData 
from time import sleep 
import re
from scrapy.http import Request
class PriceDekho(CrawlSpider):
    name = "pricedekho"
    allowed_domains = ["pricedekho.com"]
    start_urls = [
        "http://mobiles.pricedekho.com"
    ]
    def parse(self, response):
		'''
		sites=Field()
		price=Field()
		siteName=Field()
		'''
		hxs = HtmlXPathSelector(response)
		item = MetaSitesData()
		toyield=True
		sites = hxs.select("//div[@id='DescComparePrices']/ul")
		item['url']=response.url.split('?')[0]
		try:
			item['name'] = hxs.select("//div[@class='FloatLeft PaddingL250']/h1/span/text()").extract()[0]
			item['price'] = hxs.select("//div[@class='Rate']/text()").extract()
		except:
			toyield=False
		sitelist=[]
		for site in sites:
			siteObj={}
			try:
				siteObj['siteName'] = site.select("//div[@class='Clear']/a/img/@alt").extract()
				print site.select("//div[@class='Clear']/a/img/@alt").extract()
			except:
				siteObj['siteName']=''
			try:
				siteObj['url'] = site.select("//div[@class='Clear']/a//@href").extract()
				print site.select("//div[@class='Clear']/a//@href").extract()
			except:
				siteObj['url']=''
			sitelist.append(siteObj)
		item['sites']=sitelist	
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(self.start_urls[0]+url, callback=self.parse)
			except:
				print url
		if toyield:
			yield item
		sleep(2)
		