from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import MetaSitesData
from time import sleep 
import re
from scrapy.http import Request
class MySmartPriceSpider(CrawlSpider):
    name = "tolmol"
    allowed_domains = ["in.tolmol.com"]
    start_urls = [
        "http://in.tolmol.com"
    ]
    def parse(self, response):
		'''
		rating = Field()
		noOfReviews=Field()
		productID=Field()
		category=Field()
		sites=Field()
		
		
		
		
		
		price=Field()
		availability = Field()
		deliveryDays = Field()
		siteName=Field()
		siteLogo=Field()
		siteID=Field()
		minShippingDays=Field()
		maxShippingDays=Field()

		'''
		hxs = HtmlXPathSelector(response)
		item = MetaSitesData()
		toyield=True
		sites = hxs.select("//div[@class='pt_row']")
		item['url']=response.url.split('?')[0]
		try:
			item['name'] = hxs.select("//div[1]/h1/text()").extract()[0]
		except:
			toyield=False
		try:
			item['price'] = hxs.select("//div[1]/p[@id='deal']/span[@class='price']/text()").extract()
		except:
			toyield=False
        
		try:
			item['brand']= hxs.select("//div[@id='bcrumb']").extract().split('&gt;')[1].strip()
		except:
			item['brand']=''
		try:
			details= hxs.select("//div[1]/span[@id='short']/text()").extract()[0]
			det=''
			for detail in details:
				det=det+" "+detail.strip()
			item['details'] =det	
		except:
			item['details']=''
		try:
			item['images']=hxs.select("//img[@id='image3']/@src").extract()
		except:
			item['images']=''
		try:
			category=hxs.select("//div[@class='CommonBlock']").extract()
			#item['category']=category.split('&gt;')[0].strip()
		except:
			item['category']=''
		try:
			item['noOfReviews']=int(re.sub("[\D]","",hxs.select("/text()").extract()[0]))
		except:
			item['noOfReviews']=''
		try:
			item['rating']=float(hxs.select("//h2[1]/img/@src/text()").extract()[0])
		except:
			item['rating']=0
	
		sitelist=[]
		for site in sites:
			siteObj={}
			try:
				siteObj['price']= site.select("//div[@class='prc']/h6/span[@class='price']/text()").extract()[0]
			except:
				siteObj['price']=-1
			try:
				siteObj['siteName'] = site.select("//div[@id='s_name_Deals @ Door']/div[@class='mer']/a[1]/img/@src").extract()[0]
			except:
				siteObj['siteName']=''
			try:
				siteObj['url'] = site.select("//div[@id='s_name_Deals @ Door']/div[@class='mer']/a[1]/@href").extract()[0].split('?url=')[1]
			except:
				siteObj['url']=''

			try:
				shipping= re.sub("[\D]","",site.select("//div[@class='lcontent']/text()").extract()[0].strip())
				if shipping!='':
					siteObj['shippingCost'] =shipping
				else:
					siteObj['shippingCost'] =0
			except:
				siteObj['shippingCost'] =-1
			sitelist.append(siteObj)
		item['sites']=sitelist	
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(self.start_urls[0]+url, callback=self.parse)
			except:
				print url
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(url, callback=self.parse)
			except:
				print url
		if toyield:
			yield item
		sleep(2)
		