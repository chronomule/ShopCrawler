from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import MetaSitesData
from time import sleep 
import re
from scrapy.http import Request
class MySmartPriceSpider(CrawlSpider):
    name = "mysmartprice"
    allowed_domains = ["mysmartprice.com"]
    start_urls = [
        "http://www.mysmartprice.com"
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
			item['name'] = hxs.select("//div[@class='item_title']/h2/text()").extract()[0]
		except:
			toyield=False
		try:
			item['price'] = int(re.sub("[\D]",'',hxs.select("//div[@class='pricetag']/text()").extract()[1]))
		except:
			toyield=False
        
		try:
			item['brand']= hxs.select("//div[@class='pt_meta_topunit']/div[@class='alignleft']").extract()[0].split(
'&gt;')[1].strip()
		except:
			item['brand']=''
		try:
			details= hxs.select("//div[@class='detail_text']/p").extract()
			det=''
			for detail in details:
				det=det+" "+detail.strip()
			item['details'] =det
			
		except:
			item['details']=''
		try:
			item['images']=hxs.select("//div[@class='pt_meta_head']//img/@src").extract()[0]
		except:
			item['images']=''
		try:
			category=hxs.select("//div[@class='alignleft']/text()").extract()[0]
			item['category']=category.split('&gt;')[0].strip()
		except:
			item['category']=''
		try:
			item['noOfReviews']=int(re.sub("[\D]","",hxs.select("//a[@href='#review-details-name']/text()").extract()[0]))
		except:
			item['noOfReviews']=''
		try:
			item['rating']=float(hxs.select("//div[@class='item_review_text']/b/text()").extract()[0])
		except:
			item['rating']=0
	
		sitelist=[]
		for site in sites:
			siteObj={}
			try:
				siteObj['price']=float(re.sub("[\D]","",site.select("table/tr[1]/td[2]/b/text()").extract()[0]).strip())
			except:
				siteObj['price']=-1

			
			try:
				siteObj['siteName'] = site.select('table/tr/td[1]/a/img/@alt').extract()[0]
			except:
				siteObj['siteName']=''
			try:
				siteObj['url'] = site.select('table/tr/td[5]/a/@href').extract()[0].split('?url=')[1]
			except:
				siteObj['url']=''

			try:
				shipping= re.sub("[\D]","",site.select('table/tr[1]/td[4]/text()').extract()[0].strip())
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
		