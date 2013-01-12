from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Gadgetsguru(CrawlSpider):
	name = "gadgetsguru"
	allowed_domains = ["www.gadgetsguru.com"]
	start_urls = [
		"http://www.gadgetsguru.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'gadgetsguru'
		
		toyield=1
		try:
			#name: String
			name = hxs.select("//td[@class='mGreen']/b/text()").extract()
			name1 = str(name)
			name2 = name1.replace("[u'","")
			name3 = name2.replace("']","")
			item['name']= name3
			#name: Integer
		except:
			toyield=0
		try:
			price = hxs.select("//tr[@class='hBlue']//td[@align='right']/b/text()").extract()
			price1 = str(price)
			price2 = price1.replace("[u'","")
			price3 = price2.replace(".00']","")
			item['price'] = int(price3)		#srch4 stores the price
			
		except:
			toyield=0
		try:
			ship = str(hxs.select("//div[@style=' padding-left:20px; padding-right:15px']/text()").extract())
			ship1 = ship.replace("\\r\n ","")
			ship2 = ship1.replace("\\r\\n","")
			ship3 = ship2.replace("             ","")
			ship4 = ship3.replace(".      ","")
			ship5 = ship4.find("to")
			ship6 = ship4[ship5-2]
			ship7 = ship4[ship5+3]
			item['minShippingDays'] = int(ship6)
			item['maxShippingDays'] = int(ship7)
		except:
			item['minShippingDays'] = -1
			item['maxShippingDays'] = -1
		
		try:
			rat = str(hxs.select("//div[@class='hGray']//img/@src").extract())
			rat1 = rat.find("-")
			rat2 = rat[rat1+1:]
			rat3 = rat2.replace(".png","")
			rat4 = rat3.replace("']","")
			item['rating'] = float(rat4)
		except:
			item['rating'] = -1
			
		try:
			upc = str(hxs.select("//span[@class='hBlueWithBg']/text()").extract())
			upc1 = upc.find(":")
			upc2 = upc[upc1+1:]
			upc3 = upc2.replace("']","")
			item['upc'] = int(upc3)
		except:
			item['upc'] = 0
			
		try:
			trap =[]
			b = []
			c = []
			sp = {}
			specs = str(hxs.select("//td[@class='spec']//p/text()").extract())
			specs1 = specs.replace("\\xa0","")
			specs2 = specs1.split(", ")
			for counter in specs2:
				trap.append(counter)
			for counter1 in trap:
				if counter1.find("-")!=-1:
					a = counter1.find("-")
					c = counter1[a+1:]
					if a!=2:
						b = counter1[:a]
						sp[b] = c
			item['specs'] = sp		#Stores the specs list
		except:
			item['specs'] = []
		try:
			warnj = []
			war = str(hxs.select("//td[@class='spec']//p//strong/text()").extract())
			war1 = war.find("Warranty")
			war2 = war[war1:]
			war3 = war2.find("-")
			war4 = war2[war3:]
			war5 = war4.find("Warranty")
			war6 = war4[:war5]
			war7 = war6.replace("-\\xa0","")
			war8 = war7.replace("' ","")
			if war8.find("Year")!=-1:
				war9 = war8.find("Year")
				war10 = war8[:war9]
				if war10.find("One")!=-1:
					war11 = 1
				if war10.find("Two")!=-1:	
					war11 = 2
				if war10.find("Three")!=-1:	
					war11 = 3
				if war10.find("Four")!=-1:	
					war11 = 4
				if war10.find("Five")!=-1:	
					war11 = 5
				if war10.find("Six")!=-1:	
					war11 = 6
				if war10.find("Seven")!=-1:	
					war11 = 7
				if war10.find("Eight")!=-1:	
					war11 = 8
				if war10.find("Nine")!=-1:	
					war11 = 9
				item['warrenty'] = war11*12
					
			if war8.find("Years")!=-1:
				war9 = war8.find("Years")
				war10 = war8[:war9]
				if war10.find("One")!=-1:
					war11 = 1
				if war10.find("Two")!=-1:	
					war11 = 2
				if war10.find("Three")!=-1:	
					war11 = 3
				if war10.find("Four")!=-1:	
					war11 = 4
				if war10.find("Five")!=-1:	
					war11 = 5
				if war10.find("Six")!=-1:	
					war11 = 6
				if war10.find("Seven")!=-1:	
					war11 = 7
				if war10.find("Eight")!=-1:	
					war11 = 8
				if war10.find("Nine")!=-1:	
					war11 = 9
				item['warrenty'] = war11*12
				
			if war8.find("Months")!=-1:
				war9 = war8.find("Months")
				war10 = war8[:war9]
				if war10.find("One")!=-1:
					war11 = 1
				if war10.find("Two")!=-1:	
					war11 = 2
				if war10.find("Three")!=-1:	
					war11 = 3
				if war10.find("Four")!=-1:	
					war11 = 4
				if war10.find("Five")!=-1:	
					war11 = 5
				if war10.find("Six")!=-1:	
					war11 = 6
				if war10.find("Seven")!=-1:	
					war11 = 7
				if war10.find("Eight")!=-1:	
					war11 = 8
				if war10.find("Nine")!=-1:	
					war11 = 9
				item['warrenty'] = war11
		except:
			item['warrenty'] = -1
		images=[]
		try:
			images=hxs.select("//img[@id='ctl00_cphGG_frmSpec_imgL']/@src").extract()
			#name: StringList
			
			item['images'] = images
		except:
			item['images']= []
		item['category'] = []
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteID'] = 'gadgetsguru'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]
		item['siteLogo'] = hxs.select("//area[@title='Gadgetsguru Logo']/@href").extract()
		item['shippingCost']=0
		item['availability'] = -3
		item['brand']=' '
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