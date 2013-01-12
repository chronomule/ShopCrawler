from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Koovs(CrawlSpider):
	name = "koovs"
	allowed_domains = ["www.koovs.com"]
	start_urls = [
		"http://www.koovs.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'koovs'
		
		toyield=1
		try:
			#name: String
			name = hxs.select("//div[@class='detail_right_inn']/h1/text()").extract()[0].strip()
			item['name']= name
			#name: Integer
		except:
			toyield=0
		try:
			price = re.sub('\D','',re.sub('\.00','',str(hxs.select("//span[@id='ContentMain_lblYourPrice']//text()").extract())))
			item['price'] = int(price)
			    #Price stored here
		except:
			toyield=0
		try:
			store = []
			b = hxs.select("//div[@id='country5']/ul/text()").extract()
			c = str(b)
			d = c.split(",")
			for counter in d:
				if counter.find("Delivery")!=-1:
					item['maxShippingDays'] = int(counter[21])
					item['minShippingDays'] = -1
		except:
			item['maxShippingDays'] = -1
			item['minShippingDays'] = -1
			
		try:
			for counter in d:
				if counter.find("Warranty")!=-1:
					if counter.find("Years")!=-1 or counter.find("years")!=-1 or counter.find("Year")!=-1:
						item['warrenty'] = int(counter[5])*12
					elif counter.find("Months")!=-1 or counter.find("months")!=-1 or counter.find("Month")!=-1 or counter.find("month")!=-1:
						item['warrenty'] = int(counter[5])		
		except:
			item['warrenty'] = -1
			
		try:
			#name: StringList
			details =  hxs.select("//div[@id='country1']/p[3]/span/span/span/text()").extract()
			item['details']="".join(details)
		except:
			item['details']=det		
			
		images=[]
		try:
			images=hxs.select("//div[@class='main_image']/div/img/@src").extract()
			#name: StringList
			images.extend(hxs.select("//a[@id='thumb_0']/img/@src").extract())
			
			item['images'] = images
		except:
			item['images']=[]
			
		try:
			#name: StringList
			categories = hxs.select("//div[@class='breadcrumbBlk']//text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
		item['specs'] = []
		try:
			avail  =hxs.select("/html/body/div[2]/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/text()").extract()
			avail1 = str(avail)
			if avail1.find("In Stock.")!=-1:
				item['availability'] = 1
			else:
				item['availability'] = -1
		except:
			item['availability'] = -1
			
		try:
			rating = hxs.select("//div[@class='kv-stars']/@title").extract()
			rating1 = str(rating)
			rating2 = rating1[3]
			item['rating'] = int(rating2)
		except:
			item['rating'] = -1
		
		item['brand']=' '
		item['upc']=0
			
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteID'] = 'dailyobjects'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]
		item['siteLogo'] = hxs.select("//a[@class='koovs-logo']/img/@src").extract()
		
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