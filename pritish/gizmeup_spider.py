from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
import itertools

class Gizmeup(CrawlSpider):
	name = "gizmeup"
	allowed_domains = ["gizmeup.com"]
	start_urls = [
		"http://gizmeup.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'gizmeup'
		
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='product-info']/h1/text()").extract()[0].strip()
			#name: Integer
		except:
			item['name'] = " "
		try:
			price = hxs.select("//span[@id='sec_discounted_price_1220']/text()").extract()[0]
			price1 = str(price).find(",")
			price2 = price[:price1]  #Stores the digit/digits before the comma
			price3 = price[price1+1:]
			price4 = price3.find(".")
			price5 = price3[:price4]
			price6 = str(price2)+str(price5)
			price7 = int(price6)
			item['price'] = price7  #Stores the price
			#update to remove the instant cashback
		except:
			item['price'] = -1
		try:	
			dep =[]
			desc = hxs.select("//div[@id='content_block_description']//ul/li/text()").extract()
			item['details'] = desc
		except:
			item['details'] = []
		try:
			desc1 = str(desc).split(",")
			for counter in desc1:
				if counter.find("Years")!=-1:
					item['warrenty'] = counter[3]
				elif counter.find("Months")!=-1:
					item['warrenty'] = counter[3]
		except:
			item['warrenty'] = -1
		
		try:
			#name: StringList
			categories = hxs.select("//div[@class='breadcrumbs']//text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
			images=[]
		try:
			images=hxs.select("//a[@id='det_img_link_1220_2702']/img/@src").extract()
			item['images'] = images
		except:
			item['images']=[]
			
		try:
			spd = []
			spdl = []
			specleft = hxs.select("//p[@class='MsoNormal']//text()").extract()
			count = 2
			for counter in specleft:
				if count%2==0:
					spdl.append(counter)
					count+=1
				else:
					spd.append(counter)
					count+=1
			spdk = {}
			spdk = dict(zip(spd,spdl))
			item['specs'] =spdk
		except:
			item['specs'] = []
			
		item['brand']=' '	
		
		item['shippingCost']=0
		try:
			avail = hxs.select("//span[@id='in_stock_info_1220']//text()").extract()
			if avail=="In stock":
				item['availability'] = 1
			else:
				item['availability'] = -1
		except:
			item['availability'] = -3
			
		item['rating'] = -1
		
		item['minShippingDays']= -1
		item['maxShippingDays']= -1
		item['upc']=0
			
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteID'] = 'gizmeup'
		item['supportEMIInstallment'] = False   #l order is more then 4000
		item['supportCashOnDelivery'] = False     #his to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]
		item['siteLogo'] =hxs.select("//div[@class='gudz_logo']//img/@src").extract()
		
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
		
				
				
			
		yield item
		
		sleep(2)
		