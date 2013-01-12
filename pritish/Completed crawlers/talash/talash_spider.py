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

class Talash(CrawlSpider):
	name = "talash"
	allowed_domains = ["www.talash.com"]
	start_urls = [
		"http://www.talash.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'talash'
		
		toyield=0
		try:	
			#name: String
			item['name'] = hxs.select("//h1/text()").extract()[0].strip()
			check = str(item['name'])
			toyield+=1
		except: 
			toyield = 0
			#name: Integer
		try:
			price = re.sub('\D',"",re.sub('\.00',"",str(hxs.select("//span[@class='VariationProductPrice SalePrice']//text()").extract())))
			item['price'] = int(price)
			if isinstance(item['price'],int)==1:
				toyield+=1
			item['price'] = toyield
			#update to remove the instant cashback
		except:
			toyield=0
		
		#HAVE NO IDEA WHAT THE PROBLEM IS HERE!!!!!!!
		image1 = hxs.select("//a[@class='external']/@href").extract()
		item['images'] = image1
		
			
		try:
			#name: StringList
			categories = hxs.select("//div[@id='Breadcrumb']//text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='/':
					cat.append(category.strip())
			cat.append(item['name'])
			item['category']=cat
		except:
			item['category']=[]
		
		try:
			specf = []
			specs = hxs.select("//div[@class='prodescr']//li//text()").extract()
			for countin in specs:
				specf.append(countin.strip())
			item['specs'] = specf
		except:
			item['specs'] = []
			
		try:
			spc = " "
			srch = "Warranty"
			for countones in specf:
				store = countones
				if store.find(srch)>0:
					store2 = store[0] #Stores the number
					store3 = store[2:]
					store4 = store3.find(spc)
					store5 = store3[:store4]  #Stores the word
					if store5=="Months" or store5=="Month":
						store5 = int(store2)*12
						item['warrenty'] = store5
					else:
						store5 = int(store2)*1
						item['warrenty'] = store5
				else:
					item['warrenty'] = []
		except:
			item['warrenty'] = []
		item['shippingCost']=0
		try:
			srp = "In Stock"
			aval = hxs.select("//strong[@class='available_new']//text()").extract()
			if aval.srch(srp)>0:
				item['availability'] = 1
			else:
				item['availability'] = -1
		except:
			item['availability'] = -1
			
		try:
			item['brand'] = hxs.select("//span[@class='Value']/a/text()").extract()
		except:
			item['brand'] = ' '
			
			
		item['maxShippingDays'] = 5
		item['minShippingDays'] = -1
		
		try:
			#name:Integer
			item['upc'] = int(re.sub("[\D]",'',hxs.select("//tr[@class='odd'][2]").extract()))
		except:
			item['upc']=0
			
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] = hxs.select("//a[@class='checkoutalllogo']/img/@src").extract()
		item['siteID'] = 'dailyobjects'
		item['supportEMIInstallment'] = True #if total order is more then 4000
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
				
		

		
		
				
		
		
		sleep(2)