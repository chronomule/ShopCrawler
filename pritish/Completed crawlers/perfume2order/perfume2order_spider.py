from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Perfume2order(CrawlSpider):
	name = "perfume2order"
	allowed_domains = ["www.perfume2order.com"]
	start_urls = [
		"http://www.perfume2order.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'perfume2order'
		
		toyield=0
		try:
			#name: String
			name = hxs.select("//span[@id='ctl00_RightContent_UC_PerfumeDetails_LBL_Perfume_name']/text()").extract()[0].strip()
			item['name'] = name
			check = str(name)
			if len(check)!=0:
				toyield+=1
			#name: Integer
		except:
			toyield=0
		try:
			price = str(hxs.select("//span[@id='ctl00_RightContent_UC_PerfumeDetails_LBL_OPRICE']/text()").extract())
			pr1 = price.find("|")
			pr2 = price[:pr1-1]
			pr3 = re.sub('\D',"",pr2)
			item['price'] = int(pr3)	#srch4 stores the price
			if isinstance(item['price'],int)==1:
				toyield+=1
		except:
			toyield=0
			
		try:
			br = hxs.select("//span[@id='ctl00_RightContent_UC_PerfumeDetails_LBL_Designer_Name']/text()").extract()[0].strip()
			item['brand'] = br
		except:
			item['brand'] = ' '
			
		try:
			upc = str(hxs.select("//span[@id='ctl00_RightContent_UC_PerfumeDetails_lblPcode']/text()").extract())
			item['upc'] = int(upc)
		except:
			item['upc'] = 0
			
		
		try:
			imge = hxs.select("//img[@id='ctl00_RightContent_UC_PerfumeDetails_scMainImgId']/@src").extract()
			imge.extend(hxs.select("//img[@id='ctl00_RightContent_UC_PerfumeDetails_smallMainImgId']/@src").extract())
			item['images'] = imge
		except:
			item['images'] = []
			
			
		try:
			cat = []
			cat.append(item['name'])
			item['category'] = cat
		except:
			item['category'] = []
			
		try:
			item['details'] = hxs.select("//span[@class='Perfume_description']/text()").extract()
		except:
			item['details'] = []
	
			
		item['specs'] = []
		
		item['shippingCost'] = -1
		item['minShippingDays'] = -1
		item['maxShippingDays'] = -1
		item['warrenty'] = -1
		item['availability'] = -3
		item['rating'] = -1
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://www.perfume2order.com/RotateImages/Logo_new_banner.png'
		item['siteID'] = 'perfume2order'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportReplacement'] = 30
		item['cities'] = []
		item['keyword'] = []
		item['supportCashOnDelivery'] = -1
			
			
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
		
		