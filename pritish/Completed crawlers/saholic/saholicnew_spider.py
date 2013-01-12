from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Saholic(CrawlSpider):
	name = "saholic"
	allowed_domains = ["www.saholic.com"]
	start_urls = [
		"http://www.saholic.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'saholic'
		
		
		
		try:
			brand = hxs.select("//span[@class='brand']/text()").extract()[0].strip()
			item['brand'] = brand
		except:
			item['brand'] = ' ' 
			
		toyield = 0	
		try:
			name = hxs.select("//span[@class='product-name']/text()").extract()[0].strip()
			
			item['name'] = brand+" "+name
			check = str(name)
			if len(check)!=0:
				toyield+=1
		except:
			item['name'] = ' ' 
			
		try:
			price = re.sub('\D',' ',str(hxs.select("//span[@id='sp']/text()").extract()))
			item['price'] = int(price)
			if isinstance(item['price'],int)==1:
				toyield+=1
		except:
			item['price'] = 0
			
		try:
			warranty = str(hxs.select("//div[@class='warranty']/label[@class='bold']/text()").extract())
			war = re.sub(" ","",re.sub('\D',' ',warranty))
			if warranty.find("Years")!=-1 or warranty.find("Year")!=-1 or warranty.find("year")!=-1:
				war1 = int(war)*12
			if warranty.find("months")!=-1 or warranty.find("Months")!=-1:
				war1 = int(war)
			item['warrenty'] = war1
		except:
			item['warrenty'] = -1
			
		try:
			warranty = str(hxs.select("//div[@id='shipping_time']/label[@class='red']/text()").extract())
			war = re.sub(" ","",re.sub('\D',' ',warranty))
			item['minShippingDays'] = -1
			item['maxShippingDays'] = int(war)
		except:
			item['minShippingDays'] = -1
			item['maxShippingDays'] = -1
			
		try:
			img = hxs.select("//img[@id='Image1']/@src").extract()
			item['images'] = img
		except:
			item['images'] = []
			
		try:
			details = hxs.select("//div[@class='desc']/ul/li/text()").extract()
			item['details'] = details[0]		#Stores the details
		except:
			item['details'] = ' ' 
		
		
		try:
			spec = details
			sp = []
			flag = 0
			for counter in spec:
				if flag>=1:
					sp.append(counter)
					flag+=1
				else:
					flag+=1
			item['specs'] = sp
		except:
			item['specs'] = []
			
		try:
			shipco = str(hxs.select("//label[@class='red']/text()").extract())
			if shipco.find("Free Shipping")!=-1:
				item['shippingCost'] = 0
			else:
				item['shippingCost'] = -1
		except:
			item['shippingCost'] = -1
			
		try:
			#name: StringList
			categories = hxs.select("//div[@class='bread-crumbs']/a/text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>' and category.strip()!='&amp' and category.strip()!='&nbsp':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
			
		item['upc'] = 0
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] = hxs.select("//img[@title='Saholic']/@src").extract()
		item['siteID'] = 'saholic'
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