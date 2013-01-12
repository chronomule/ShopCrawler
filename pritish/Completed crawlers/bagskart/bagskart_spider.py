from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Bagskart(CrawlSpider):
	name = "bagskart"
	allowed_domains = ["www.bagskart.com"]
	start_urls = [
		"http://www.bagskart.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'bagskart'
		
		toyield=0
		try:
			#name: String
			name = (hxs.select("//span[@class='product-name']/text()").extract())[0].strip()
			item['name'] = name
			check = str(name)
			if len(check)!=0:
				toyield+=1
			#name: Integer
		except:
			toyield=0
			
		try:
			price = str(hxs.select("//span[@class='spcl-price']/text()").extract())
			price1 = price.replace("\\u20a8. ","")
			price2 = price1.replace("[u'","")
			price3 = price2.replace("']","")
			price4 = price3.replace(".00","")
			price5 = price4.replace(",","")
				
			item['price'] = int(price5)	#srch4 stores the price
			if isinstance(item['price'],int)==1:
				toyield+=1
			
		except:
			toyield=0
			
		try:
			images=hxs.select("//a[@ id='MagicZoomPlusImagemagictoolbox1']/img/@src").extract()
			#name: StringList
			img1 = hxs.select("//a[@class='MagicThumb-swap']/img/@src").extract()
			if img1!=images:
				images.extend(hxs.select("//a[@class='MagicThumb-swap']/img/@src").extract())
			item['images'] = images
		except:
			item['images']=[]
			
		try:
			cod = str(hxs.select("//span[@class='top-free']/text()").extract())
			if cod.find("Cash On Delivery")!=-1:
				item['supportCashOnDelivery'] = True
		except:
			item['supportCashOnDelivery'] = False
			
		try:
			if cod.find("Free delivery in india")!=-1:
				item['shippingCost'] = 0
		except:
			item['shippingCost'] = -1
			
			
		try:
			#name: StringList
			categories = hxs.select("//ul[@class='breadcrumbs']//li//text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>' and category.strip()!='/':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
			
		try:
			ship = str(hxs.select("//span[@class='free-deliv']//span[@class='bottom-free']/text()").extract())
			ship1 = ship.find("-")
			ship2 = ship[ship1-2]
			ship3 = ship[ship1+2]
			item['minShippingDays'] = int(ship2)
			item['maxShippingDays'] = int(ship3)
		except:
			item['minShippingDays'] = -1
			item['maxShippingDays'] = -1
		
		try:
			details = str(hxs.select("//span[@class='short-description']/text()").extract())
			details1 = details.replace('\n',"")
			details2 = details1.replace('\t',"")
			details3 = details2.replace('\\n',"")
			details4 = details3.replace('\\t',"")
			details5 = details4.replace("u'   ","")
			details6 = details5.replace(" ', ","")
			details7 = details6.replace("u''","")
			details8 = details7.replace('\\u',"")
			item['details'] = details8		#Stores the details
		except:
			item['details'] = []
			
		try:
			a = []
			b = []
			specleft = hxs.select("//tr[@class='first odd']/td[@class='label']/text()").extract()
			specright = hxs.select("//tr[@class='first odd']/td[@class='data last']/text()").extract()
			for counter in specleft:
				a.append(counter)
			for counter1 in specright:
				b.append(counter1)
			s = {}
			s = dict(zip(a,b))
			item['specs'] = specleft
		except:
			item['specs'] = []
			
		item['upc'] = 0	
		item['availability'] = -3
		item['rating'] = -1
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://www.bagskart.com/skin/frontend/default/helloone_bags/images/logo.gif'
		item['siteID'] = 'bagskart'
		item['supportEMIInstallment'] = True #if total order is more then 4000
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