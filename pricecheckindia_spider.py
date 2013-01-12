from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import MetaSitesData
from time import sleep 
import re
from scrapy.http import Request
class MySmartPriceSpider(CrawlSpider):
    name = "pricecheckindia"
    allowed_domains = ["pricecheckindia.com"]
    start_urls = [
        "http://www.pricecheckindia.com"
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
		sites = hxs.select("//div[@id='priceTable']/table/tbody/tr[@class='tableRow']")
		
		item['url']=response.url.split('?')[0]
		try:
			item['name'] = hxs.select("//div[@id='productMain']/h1/text()").extract()[0]
		except:
			toyield=False
		sitelist=[]
		for site in sites:
			siteObj={}
			try:
				siteObj['siteName'] = site.select('td[1]/a/img/@alt').extract()[0]
				print site.select('//td[1]/a/img/@alt').extract()[0]
			except:
				siteObj['siteName']=''
			try:
				siteObj['url'] = site.select('td[4]/a/@href').extract()[0]
				print site.select('td[4]/a/@href').extract()[0]
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
		sleep(60)
		