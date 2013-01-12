from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Zoomin(CrawlSpider):
	name = "next"
	allowed_domains = ["www.next.co.in"]
	start_urls = [
		"http://www.next.co.in"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'next'
		
		toyield=1
		try:
			#name: String
			name = hxs.select("//div[@class='product-name']/h1//text()").extract()[0].strip()
			item['name']= name
			#name: Integer
		except:
			toyield=0
		try:
			price = hxs.select("//p[@class='special-price']/span//text()").extract()[0].strip()
			price1 = str(price)
			price2 = price.find("Rs")
			price3 = price[price2+3:]
			price4 = price3.find(",")
			price5 = price3[:price4]
			price6 = price3[price4+1:]
			price7 = price5+price6
			item['price'] = int(price7)		#price7 stores the price
			
		except:
			toyield=0
			
		try:	
			#name: String
			warrenty=hxs.select("//div[@class='product-main-info']/p[3]/text()").extract()
			war = str(warrenty)
			if war.find("Years")!=-1 or war.find("Year")!=-1 or war.find("year")!=-1 or war.find("years")!=-1:
				item['warrenty'] = int(war[3])*12
			elif war.find("Months")!=-1:
				item['warrenty'] = int(war[3])
		except:
			item['warrenty']=-1
		
		images=[]
		try:
			images=hxs.select("//p[@class='more-views']//img/@src").extract()
			#name: StringList
			images.extend(hxs.select("//div[@class='more-views']//img/@src").extract())
			
			item['images'] = images
		except:
			item['images']=[]
			
		item['category'] = []
		
		try:
			#name: StringList
			details =  hxs.select("//div[@class='std']/text()").extract()
			de1 = str(details)
			de2 = de1.find("A")
			de3 = de1[de2:]
			item['details']="".join(de3)
		except:
			item['details']=det			
	
		try:
			specleft = hxs.select("//tr[@class='first odd']/td//text()").extract()
			item['specs'] = specleft
		except:
			item['specs'] = []
			
		# NEED TO REWORK THIS BIT. ISSUE EXISTS WITH THE SPECS LIST

		item['shippingCost']=0
		item['availability'] = -3
		
		try:
			midship = hxs.select("//div[@class='tab-content']/p//text()").extract()
			midstr = str(midship)
			midstra = midstr.find("-")
			midstrb = midstr[midstra-1]
			midstrc = midstr[midstra+1]
			item['maxShippingDays'] = int(midstrc)
			item['minShippingDays'] = int(midstrb)
		except:
			item['minShippingDays'] = -1
			item['maxShippingDays'] = -1
			
		item['rating'] = -1
		try:
			#name:Integer
			item['upc'] = int(re.sub("[\D]",'',hxs.select("//tr[@class='odd'][2]").extract()))
		except:
			item['upc']=0
			
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteID'] = 'dailyobjects'
		item['supportEMIInstallment'] = False #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]
		item['siteLogo'] = hxs.select("//img[@alt='Next logo']/@src").extract()
		if toyield:
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
		
		sleep(2)