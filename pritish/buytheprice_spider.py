from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Buytheprice(CrawlSpider):
	name = "buytheprice"
	allowed_domains = ["www.buytheprice.com"]
	start_urls = [
		"http://www.buytheprice.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'buytheprice'
		
		try:
			name = hxs.select("//h1[@class='biglineh2']/text()").extract()[0].strip()
			
			item['name'] = name
		except:
			item['name'] = ' ' 
			
		try:
			brand = str(name)
			brand1 = brand.find(" ")
			brand2 = brand[:brand1]
			item['brand'] = brand2
		except:
			item['brand'] = ' '
			
		try:
			price = re.sub(" ","",re.sub('\D',' ',str(hxs.select("//span[@itemprop='price']/text()").extract())))
			item['price'] = int(price)
		except:
			item['price'] = 0
			
		try:
			warranty = re.sub(" ","",re.sub('\D',' ',str(hxs.select("//span[@class='p-biggray']/text()").extract())))
			war = str(hxs.select("//span[@class='p-biggray']/text()").extract())
			if war.find("Year")!=-1 or war.find("Years")!=-1 or war.find("year")!=-1:
				war1 = int(warranty)*12
			if war.find("Months")!=-1 or war.find("months")!=-1:
				war1 = int(warranty)
				
			item['warrenty'] = war1
		except:
			item['warrenty'] = -1
			
		try:
			avail = str(hxs.select("//div[@class='iostock']/text()").extract())
			if avail.find("In Stock")!=-1:
				item['availability'] = 1
		except:
			item['availability'] = -1
			
		try:
			ship = str(hxs.select("//div[@class='prblinfo']/text()").extract())
			ship1 = ship.find("-")
			ship2 = ship[ship1-1]
			ship3 = ship[ship1+1]
			item['minShippingDays'] = int(ship2)
			item['maxShippingDays'] = int(ship3)
		except:
			item['minShippingDays'] = -1
			item['maxShippingDays'] = -1
			
		try:
			img = str(hxs.select("/html/body/table/tbody/tr[4]/td/div/div/table/tbody/tr[4]/td/table/tbody/tr[3]/td/div/img/@src").extract())
			item['images'] = img
		except:
			item['images'] = []
			
		try:
			cod = str(hxs.select("//div[@class='payops']/text()").extract())
			emi = cod
			if cod.find("Cash on Delivery")!=-1:
				item['supportCashOnDelivery'] = True
			else:
				item['supportCashOnDelivery'] = False
		except:
			item['supportCashOnDelivery'] = False
			
		try:
			if emi.find("EMI")!=-1:
				item['supportEMIInstallment'] = True
			else:
				item['supportEMIInstallment'] = False
		except:
			item['supportEMIInstallment'] = False
			
		item['details'] = []
		try:
			a = []
			b = []
			prodleft = hxs.select("//td[@class='prodspecleft']/text()").extract()
			prodright = hxs.select("//td[@class='prodspecright']/text()").extract()
			for counter in prodleft:
				a.append(counter)
			for counter2 in prodright:
				b.append(counter2)
			specser = {}
			specser = dict(zip(a,b))
			item['specs'] = specser
		except:
			item['specs'] = []
			
		item['upc'] = 0
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] = hxs.select("//div[@id='logo']//img/@src").extract()
		item['siteID'] = 'buytheprice'
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]
		

		
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