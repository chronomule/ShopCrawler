from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Brandsknot(CrawlSpider):
	name = "brandsknot"
	allowed_domains = ["www.brandsknot.com"]
	start_urls = [
		"http://www.brandsknot.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'brandsknot'
		
		try:
			name = hxs.select("//td[@width='85%']/text()").extract()[0].strip()
			
			item['name'] = name
		except:
			item['name'] = ' ' 
			
		try:
			price = re.sub('\D',"",re.sub('\.00',' ',str(hxs.select("//input[@id='txtprice']/@value").extract())))
			item['price'] = int(price)
		except:
			item['price'] = 0
			
		try:
			#name: StringList
			categories = hxs.select("//td[@colspan='2']/a/text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>' and category.strip()!='&amp':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
			
		try:
			images = hxs.select("//img[@id='imges']/@src").extract()
			item['images'] = images
		except:
			item['images'] = []
			
		try:
			warranty = str(hxs.select("//td[@style='padding-left:5px; padding-right:5px;']/text()").extract())
			war = re.sub('\D',"",warranty)
			if warranty.find("Years")!=-1 or warranty.find("years")!=-1 or warranty.find("year")!=-1:
				item['warrenty'] = int(war)*12
			elif warranty.find("Months")!=-1 or warranty.find("months")!=-1:
				item['warrenty'] = int(war)
		
		except:
			item['warrenty'] = -1
			
		try:
			specs = hxs.select("//span[@style='font-family: Verdana; ']/span[@style='font-size: small; ']/text()").extract()
			item['specs'] = specs
		except:
			item['specs'] = []
		
		item['details'] = []
		item['upc'] = 0
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] = hxs.select("//a[@href='default.aspx']/img/@src").extract()
		item['siteID'] = 'brandsknot'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportCashOnDelivery'] = False  #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]	
		item['minShippingDays'] = -1
		item['maxShippingDays'] = -1
		item['availability'] = -1
		
		try:
			brand = str(name)
			brand1 = brand.find(" ")
			brand2 = brand[:brand1]
			item['brand'] = brand2
		except:
			item['brand'] = ' '
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
