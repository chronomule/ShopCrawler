from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Edigiworld(CrawlSpider):
	name = "edigiworld"
	allowed_domains = ["www.edigiworld.com"]
	start_urls = [
		"http://www.edigiworld.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'edigiworld'
		
		toyield=0
		try:
			#name: String
			name = hxs.select("//div[@class='ctl_aboutbrand']/h1/text()").extract()[0].strip()
			item['name'] = name
			check = str(name)
			if len(check)!=0:
				toyield+=1
			#name: Integer
		except:
			toyield=0
		try:
			price = re.sub('\D',"",re.sub('\.00',"",str(hxs.select("//span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_lblOfferPrice']/text()").extract())))
			
				
			item['price'] = int(price)	#srch4 stores the price
			if isinstance(item['price'],int)==1:
				toyield+=1
		except:
			toyield=0
			
		try:
			br = hxs.select("//span[@class='brandlname']/text()").extract()[0].strip()
			item['brand'] = br
		except:
			item['brand'] = ' '
			
		try:
			imge = hxs.select("//a[@id='zoomImg']/@href").extract()
			item['images'] = imge
		except:
			item['images'] = []
			
		try:
			desc = str(hxs.select("//div[@id='Description']/text()").extract())
			desc1 = desc.replace('\\r\n',"")
			desc2 = desc1.replace(" ","")
			desc3 = desc2.replace('\\r\\n',"")
			item['details'] = desc3
		except:
			item['details'] = []
			
		try:
			a = []
			b = []
			d = []
			specr = str(hxs.select("//td[@class='propertylist']//text()").extract())
			specl = str(hxs.select("//td[@class='propertylist_2']/label/text()").extract())
			for counter in specr.split(","):
				a.append(counter)
			for counter1 in specl.split(","):
				b.append(counter1)
			for counter in b:
				p = counter.replace("\\xa0","")
				q = p.replace("[u'","u'")
				r = q.replace("]","")
				d.append(r)
			c = {}
			c = dict(zip(a,d))
			item['specs'] = c
		except:
			item['specs'] = []
			
		try:
			avail = str(hxs.select("//div[@class='instock']/text()").extract())
			if avail.find("Stock Available")!=-1:
				item['availability'] = 1
		except:
			item['availability'] = -3
			
		try:
			#name: StringList
			categories = hxs.select("//div[@id='ctl00_ContentPlaceHolder1_Breadcrum_ctl00_brdCrumbNormal']/a/text()").extract()
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
		item['upc'] = 0
		item['rating'] = -1
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://www.edigiworld.com'
		item['siteID'] = 'edigiworld'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportReplacement'] = 30
		item['cities'] = []
		item['keyword'] = []
		item['supportCashOnDelivery'] = False
		
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
				
		 
		
		
				
			
		if toyield==2:	
			yield item
		
		sleep(2)