from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Flipkart(CrawlSpider):
	name = "flipkart"
	allowed_domains = ["www.onlinebuy99.com"]
	start_urls = [
		"http://www.onlinebuy99.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'Onlinebuy99'
		
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='product-shop']/div[@class='product-name']/h2/text()").extract()[0].strip()
			#name: Integer
			item['price'] = int(re.sub('\D','',re.sub('\.00','',hxs.select("//span[@class='price']/text()").extract()[0].encode("utf-8",'ignore'))))
		except:
			toyield=0
		try:	
			#name: String
			item['warrenty']=round(float(re.sub("[\D]"," ",hxs.select("//div[@class='mprod-warrenty']/text()").extract()[0]).strip().split(' ')[0])*12)
		except:
			item['warrenty']=-1
		images=[]
		try:
			images=hxs.select("//p[@class='product-image']/img[@id='image']/@src").extract()
			#name: StringList
		#	images.extend(hxs.select("//div[@id='mprodimg-id']/img/@src").extract())
		#	images.extend(hxs.select("//div[@class='image-wrapper']/img/@src").extract())
			
			#item['images'] = images
		except:
			item['images']=[]
		try:
			#name: StringList
			categories = hxs.select("//div[@class='breadcrumbs']/ul/span/a/span/text()").extract()
			if len(categories)==0:
				categories.extend(hxs.select("//div[@class='breadcrumbs']/ul//text()").extract())
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
		det=''
		try:
			#name: StringList
			details =  hxs.select("//div[@class='short-description std']/p/text()").extract()
			for detail in details:
				det=det+" "+detail.strip()
			item['details']=det
		except:
			item['details']=det
		try:
			#name: Float
			item['rating']= float(re.sub("[A-Za-z]",'',hxs.select("//div[@class='fk-stars']/@title").extract()[0]).strip())
		except:
			item['rating'] = -1
		try:
			item['brand']= hxs.select("//td[@class='data last']").extract()[0]
		except:
			item['brand']=''
		try:
			#name: String
			instock=hxs.select("//p[@class='availability']/span[@class='in-stock']/text()").extract()[0]
			outofstock = hxs.select("//p[@class='availability']/span[@class='in-stock']/text()").extract()[0]
			if instock=='In Stock.':
				item['availability'] =-3
			if instock=='Available.':
				item['availability'] =-3
			if instock=='Imported Edition.':
				item['availability'] =-3
			if outofstock=='Out of Stock':
				item['availability'] =-1
		except:
			item['availability'] = -3
		try:
			item['siteLogo'] =hxs.select("//div[@class='col-1']/h1[@id='logo']/text()").extract()[0]
		except:
			item['siteLogo']=[]
		item['shippingCost'] = 0
		item['productID'] = item['identifier']
		item['siteID'] = 'onlinebuy99'
		item['supportEMIInstallment'] = False 
		item['supportCashOnDelivery'] = False  
		item['supportReplacement'] = False	
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(self.start_urls[0]+url, callback=self.parse)
			except:
				abc=1
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(url, callback=self.parse)
			except:
				abc=1
		
		if toyield:
			yield item
		
		sleep(2)