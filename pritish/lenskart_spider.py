from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Lenskart(CrawlSpider):
	name = "lenskart"
	allowed_domains = ["www.lenskart.com"]
	start_urls = [
		"http://www.lenskart.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'lenskart'
		
		try:
			name = hxs.select("//div[@class='product-img-box']/span/text()").extract()[0].strip()
			
			item['name'] = name
		except:
			item['name'] = ' ' 
			
		try:
			price = str(hxs.select("//div[@id='r']/span/text()").extract())
			price1 = price.replace("\\u20a8. ","")
			price2 = price1.replace("[u'","")
			price3 = price2.replace("']","")
			price4 = price3.replace(".00","")
			price5 = price4.replace(",","")
			price6 = price5.replace('\\n',"")
			price7 = price6.replace('\\t',"")
			item['price'] = int(price7)
		except:
			item['price'] = 0
			
		item['supportReplacement'] = 14
		item['shippingCost'] = 0
		try:
			images = hxs.select("//a[@id='MagicZoomPlusImagemagictoolbox1']/img/@src").extract()
			images.extend(hxs.select("//a[@class='MagicThumb-swap']/@rev").extract())
			item['images'] = images
		except:
			item['images'] = []
			
		det=''
		try:
			#name: StringList
			details =  hxs.select("//div[@class='product-specs']/p/text()").extract()
			item['details']="".join(details)
		except:
			item['details']=det
			
		try:
			a=[]
			b=[]
			c={}
			specleft = hxs.select("//table[@id='product-attribute-specs-table']//td/text()").extract()
			flag=2
			for counter in specleft:
				if flag%2==0:
					a.append(counter)
					flag+=1
				else:
					b.append(counter)
					flag+=1
			c = dict(zip(a,b))
				
			item['specs'] = c
		except:
			item['specs'] = []
			
		try:
			brand = c['Product Brand']
			item['brand'] = brand
		except:
			item['brand'] = ''
			
		try:
			ship = hxs.select("//div[@class='product-specs']//li/text()").extract()
			ship1 = str(ship[0])
			ship2 = ship1.find("-")
			ship3 = ship1[ship2-1]
			ship4 = ship1[ship2+1]
			item['minShippingDays'] = int(ship3)
			item['maxShippingDays'] = int(ship4)
		except:
			item['minShippingDays'] = -1
			item['maxShippingDays'] = -1
			
		item['warrenty'] = -1
		item['upc'] = 0
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] = hxs.select("//a[@id='contact_lens']/img/@src").extract()
		item['siteID'] = 'lenskart'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportCashOnDelivery'] = True  #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]	
		item['availability'] = -1
		
		try:
			#name: StringList
			categories = hxs.select("//ul[@class='breadcrumbs']//text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='/' and category.strip()!='&amp':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
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