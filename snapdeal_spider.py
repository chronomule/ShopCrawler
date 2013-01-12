from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class letsbuy(CrawlSpider):
	name = "letsbuy"
	allowed_domains = ["www.snapdeal.com"]
	start_urls = [
		"http://www.snapdeal.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'snapdeal'
		toyield=1
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='prodtitle-head']/h1/text()").extract()[0]
			#name: Integer
			item['price'] =hxs.select("//div[@class='payInAdv']/span[@id='selling-price-id']").extract()
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//ul[@id='product-thumbs']//img/@src").extract()
		except:
			try:
				item['images']=hxs.select("//ul[@id='product-thumbs']//img/@src").extract()
			except:
				item['images']=[]
		try:
			#name: StringList
			categories = hxs.select("//div[@class='bread-crumb']/div[@class='bread-cont']").extract()
			cat=[]
			catcount=1
			for category in categories:
				if category!='snapdeal.com' and catcount!=len(categories):
					cat.append(category.strip())
				if catcount==len(categories):
					item['brand']=category.strip()
				catcount=catcount+1
				
			item['category']=cat
		except:
			item['category']=[]
			item['brand']=''
		try:
			#name: StringList
			details =  hxs.select("//dt[@class='deal-detalis-tab-cont'][1]/text()").extract()
			det=''
			for detail in details:
				if detail.strip()!='':
					det=det+" "+detail.strip()
			item['details']=det
		except:
			item['details']=''
		try:
			#name: String
			olscount=1
			ols=hxs.select("//div[@class='product-free-ship-outer']")
			for ol in ols:
				ilscount=1
				if "delivery time" in hxs.select("//div[@class='product-free-ship-outer']").extract()[0]:
					shippingdays = hxs.select("//div[@class='product-free-ship-outer']").extract()[0]
				olscount=olscount+1
			if(int(shippingdays[0])<int(shippingdays[1])):
				item['minShippingDays'] = int(shippingdays[0])
				item['maxShippingDays'] = int(shippingdays[1])
			else:
				item['minShippingDays'] = int(shippingdays[1])
				item['maxShippingDays'] = int(shippingdays[0])
			
		except:
			item['minShippingDays']=-1
			item['maxShippingDays']=-1

		try:
			#name: String
			item['warrenty'] = hxs.select("//div[@class='prod-warranty-text']/text()").extract()
		except:
			item['warrenty'] = -1
		try:
			#name: StringList
			item['specs'] = hxs.select("//table[@class='product-spec']//td[1]/text()","----->","//table[@class='product-spec']//td[2]/text()").extract()
		except:
			try:
				item['specs'] = hxs.select("//table[@class='product-spec']//td[2]/text()").extract()
			except:
				item['specs']=[]
		item['shippingCost'] = 0
		item['upc']=0
		item['upclist'] = []
		item['barcode']=0
		item['productID']=item['identifier']
		item['siteLogo']=''
		item['siteID']='snapdeal'
		item['supportEMIInstallment']=False
		item['supportCashOnDelivery']=True
		item['cities']=[]

		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(self.start_urls[0]+url,callback=self.parse)
			except:
				print "Item Unexpected error:"
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(url, callback=self.parse)
			except:
				print "Unexpected error:"
		if toyield:
			yield item
		sleep(2)
