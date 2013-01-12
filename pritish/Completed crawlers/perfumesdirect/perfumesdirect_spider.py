from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Watchkart(CrawlSpider):
	name = "perfumesdirect"
	allowed_domains = ["www.perfumesdirect.co.in"]
	start_urls = [
		"http://www.perfumesdirect.co.in"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'perfumesdirect'
		
		toyield=0
		try:
			#name: String
			name = hxs.select("//span[@id='ctl00_MainContent_lbl_ProductNmae']/text()").extract()[0].strip()
			item['name'] = name
			check = str(name)
			if len(check)!=0:
				toyield+=1
			#name: Integer
		except:
			toyield=0
		try:
			price = hxs.select("//table[@id='ctl00_MainContent_grdProductAttributes']//td//text()").extract()
			flag = 1
			for counter in price:
				if flag==4:
					store = counter
					flag+=1
				else:
					flag+=1
			store1 = str(store)
			store2 = re.sub('\D',"",store1)
			item['price'] = int(store2)	#srch4 stores the price
			if isinstance(item['price'],int)==1:
				toyield+=1
		except:
			toyield=0
			
		try:
			imge = hxs.select("//img[@id='ctl00_MainContent_imgProductImage']/@src").extract()
			item['images'] = imge
		except:
			item['images'] = []
			
		try:
			det = str(hxs.select("//span[@id='ctl00_MainContent_lblLongDescription']/text()").extract())
			det1 = det.replace("[u'","")
			det2 = det1.replace("']","")
			item['details'] = det2
		except:
			item['details'] = ' '
			
		item['specs'] = []
		item['warrenty'] = -1
		
		item['minShippingDays'] = -1
		item['maxShippingDays'] = -1
		item['shippingCost'] = 0
		item['upc'] = 0
		
		try:
			#name: StringList
			categories = hxs.select("//td[@class='breadCrumb']/a/text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home - Perfumes Online' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>' and category.strip()!='/':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
			
		item['supportCashOnDelivery'] = -1
		item['availability'] = -3
		item['rating'] = -1
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://s.dkrt.in/skin/frontend/default/helloone_wat/images/logo.png'
		item['siteID'] = 'watchkart'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportReplacement'] = 30
		item['cities'] = []
		item['keyword'] = []
		
		try:
			br = str(name)
			br1 = br.find(" ")
			br2 = br[:br1]
			item['brand'] = br2
		except:
			item['brand'] = ' '
			
		
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
		