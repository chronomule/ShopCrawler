from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Inkfruit(CrawlSpider):
	name = "inkfruit"
	allowed_domains = ["www.inkfruit.com"]
	start_urls = [
		"http://www.inkfruit.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'inkfruit'
		
		try:
			#name: String
			name = hxs.select("//div[@class='prTitleTop']//text()").extract()[0].strip()
			item['name'] = name
			#name: Integer
		except:
			toyield=0
		try:
			price = re.sub('\D','',re.sub('\.00','',str(hxs.select("//span[@class='price']//text()").extract())))
			
			item['price'] = int(price)		#srch4 stores the price
			
		except:
			toyield=0
		item['warrenty'] = -1
		
		images=[]
		try:
			images=hxs.select("//a[@id='zoom1']/img/@src").extract()
			#name: StringList
			images.extend(hxs.select("//a[@id='imgThumb']/img/@src").extract())
			images.extend(hxs.select("//a[@id='imgThumb1']/img/@src").extract())
			images.extend(hxs.select("//a[@id='imgThumb2']/img/@src").extract())
			item['images'] = images
		except:
			item['images']=images
		
		try:
			#name: StringList
			categories = hxs.select("//div[@class='newPageHeading']//text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!=':':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
		det=''
		try:
			#name: StringList
			details =  hxs.select("//div[@id='prInfo']//text()").extract()
			item['details']="".join(details)
		except:
			item['details']=det			
		
		item['specs'] = []
		item['shippingCost']=0
		item['availability'] = -3
		item['rating'] = -1
		item['minShippingDays']= -1
		item['maxShippingDays']= -1
		item['upc']=0
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteID'] = 'dailyobjects'
		item['supportEMIInstallment'] = False #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]
		item['siteLogo'] = hxs.select("//div[@id='logo']//img/@src").extract()
		
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