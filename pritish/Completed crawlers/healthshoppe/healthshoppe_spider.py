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
	name = "healthshoppe"
	allowed_domains = ["www.health-shoppe.com"]
	start_urls = [
		"http://www.health-shoppe.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'healthshoppe'
		
		toyield=0
		try:
			#name: String
			name = hxs.select("//div[@id='center-main']/h1/text()").extract()[0].strip()
			item['name'] = name
			check = str(name)
			if len(check)!=0:
				toyield+=1
			#name: Integer
		except:
			toyield=0
		try:
			price = re.sub('\D'," ",re.sub('\.00'," ",str(hxs.select("//span[@id='product_price']/text()").extract())))
				
			item['price'] = int(price)	#srch4 stores the price
			if isinstance(item['price'],int)==1:
				toyield+=1
		except:
			toyield=0
			
		try:
			det = str(hxs.select("//p//text()").extract())
			det1 = det.replace("\\n","")
			det2 = det1.replace("\\t","")
			det3 = det2.replace("\\r","")
			det4 = det3.replace("\\xa0","")
			det5 = det4.replace("u'',","")
			item['details'] = det5
		except:
			item['details'] = ' '
			
		try:
			#name: StringList
			categories = hxs.select("//div[@id='location']/a/text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>' and category.strip()!='/':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
		item['minShippingDays'] = -1
		item['maxShippingDays'] = -1
		item['warrenty'] = -1
		item['shippingCost'] = 0
		item['specs'] = []
		
		try:
			upc = re.sub('\D',"",str(hxs.select("//td[@id='product_code']/text()").extract()))
			item['upc'] = int(upc)
		except:
			item['upc'] = 0
			
		try:
			rat = str(hxs.select("//div[@class='creviews-rating-box']//div[@class='creviews-vote-bar allow-add-rate']/@title").extract())
			rat1 = rat.find(":")
			rat2 = rat[rat1:]
			rat3 = rat2[2]
			rat4 = rat2[4]
			rat5 = rat2[5]
			item['rating'] = float(rat3+"."+rat4+rat5)
		except:
			item['rating'] = -1
			
			
		try:
			images = hxs.select("//img[@id='product_thumbnail']/@src").extract()
			item['images'] = images
		except:
			item['images'] = []
			
		item['availability'] = -3
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='/skin/artistictunes_business/images/custom/hs-logo-1211.jpg'
		item['siteID'] = 'watchkart'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportReplacement'] = 30
		item['cities'] = []
		item['keyword'] = []
		
		
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