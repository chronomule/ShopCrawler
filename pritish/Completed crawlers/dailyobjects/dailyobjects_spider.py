from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Dailyobjects(CrawlSpider):
	name = "dailyobjects"
	allowed_domains = ["www.dailyobjects.com","dailyobjects.com"]
	start_urls = [
		"http://www.dailyobjects.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#string
		item['siteName'] = 'dailyobjects'
		
		toyield=0
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='product-name']//h1/text()").extract()[0].strip()
			print item['name']
			check = str(name)
			if len(check)!=0:
				toyield+=1
		except:
			toyield = 0
		try:
			#name: Integer
			item['price'] = int(re.sub('\D','',re.sub('\.00','',hxs.select("//span[@class='product-dtail-main-price']/text()").extract()[0].encode("utf-8",'ignore'))))
			print item['price']
			if isinstance(item['price'],int)==1:
				toyield+=1
			#update to remove the instant cashback
		except:
			toyield=0
		try:	
			#name: String
			str1 = hxs.select("//span[@class='warranty_viewpage']//text()").extract()[0].strip()
			str2 = str1[0]
			str3 = int(str2)*12
			item['warrenty'] = str3
		except:
			item['warrenty'] = -1
		try:
			images=hxs.select("//p[@class='product-image']/img/@src").extract()
			#name: StringList
			images.extend(hxs.select("//a[@class='fancy-zoom-gallery-link']/img/@src").extract())
			#NEED TO CHECK IF THIS LINE BELW IS NEEDED DEPENDING ON THE AVAILABILITY OF IMAGES
			images.extend(hxs.select("//div[@class='image-wrapper']/img/@src").extract())
			
			item['images'] = images
		except:
			item['images']=[]
		try:
			#name: StringList
			categories = hxs.select("//div[@class='breadcrumbs']//text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='/':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
		det=''
		try:
			#name: StringList
			details =  hxs.select("//td[@class='product_dailyobjects_detail_desc']//text()").extract()
			item['details']="".join(details)
		except:
			item['details']=det	
			
		det1=''
		try:
			#name: StringList
			speclist =  hxs.select("//div[@class='product_detail_main_tbl']//text()").extract()
			item['specs']="".join(speclist)
		except:
			item['specs']=det1
		item['shippingCost']=0
		item['availability'] = -3
		
		try:
			#name: Float
			item['rating']= float(re.sub("[A-Za-z]",'',hxs.select("//div[@class='fk-stars']/@title").extract()[0]).strip())
		except:
			item['rating'] = -1
			
		item['minShippingDays']= 2
		item['maxShippingDays']= 5
		
		try:
			#name:Integer
			item['upc'] = int(re.sub("[\D]",'',hxs.select("//tr[@class='odd'][2]").extract()))
		except:
			item['upc']=0
			
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://img5.flixcart.com/www/prod/images/flipkart_india-31804.png'
		item['siteID'] = 'dailyobjects'
		item['supportEMIInstallment'] = False #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]

		if toyield==2:
			yield item

		
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