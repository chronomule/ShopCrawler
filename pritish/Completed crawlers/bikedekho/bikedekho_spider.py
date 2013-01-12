from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
import itertools

class Bikedekho(CrawlSpider):
	name = "bikedekho"
	allowed_domains = ["www.bikedekho.com"]
	start_urls = [
		"http://www.bikedekho.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'bikedekho'
		
		toyield=0
		try:	
			#name: String
			item['name'] = hxs.select("//span[@class='float-left full-width']/h2/text()").extract()[0].strip()
			check = str(name)
			if len(check)!=0:
				toyield+=1
		except: 
			toyield = 0
			
		try:
			price = re.sub('\D',"",str(hxs.select("//span[@class='float-left widththrirtyfive']/text()").extract()))
			item['price'] = int(price)
			if isinstance(item['price'],int)==1:
				toyield+=1
			#update to remove the instant cashback
		except:
			toyield=0
			
		try:
			image = hxs.select("//div[@class='variant-product-img-in float-left']/img/@src").extract()
			image.extend(hxs.select("//div[@class='varient-page-small-pic-div']/a/img/@src").extract())
			item['images'] = image
		except:
			item['image'] = []
			
		try:
			rating = re.sub('\D',"",str(hxs.select("//span[@class='average-rating']/span/text()").extract()))
			rat = rating[0]
			rat1 = rating[1]
			rat2 = rat+"."+rat1
			item['rating'] = float(rat2)		#This stores the rating value
		except:
			item['rating'] = -1
			
		
		try:
			det = hxs.select("//div[@class='float-left model-expert-review-differ-div']/p/text()").extract()
			item['details'] = det
		except:
			item['details'] = ' '
			
			
		try:
			a = []
			b = []
			c = []
			specsleft = hxs.select("//div[@class='variant-overview-left float-left']/text()").extract()
			specsright = hxs.select("//div[@class='variant-overview-right float-left']/text()").extract()
			for counter in specsright:
				a.append(counter)
			for counter1 in a:
				de = str(counter1)
				der = de.replace('\t',"")
				der1 = der.replace('\n',"")
				der2 = der1.replace(" ","")
				b.append(der2)
			
			for counter3 in	specsleft:
				cfg = str(counter3)
				c.append(cfg)
			d = {}
			d = dict(zip(c,b))
			
				
			item['specs'] = d		#d stores the specs
		except:
			item['specs'] = []
			
		
		try:
			#name: StringList
			categories = hxs.select("//div[@class='bredcrum-first']/a/text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='New Bikes' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='/':
					cat.append(category.strip())
			cat.append(item['name'])
			item['category']=cat
		except:
			item['category']=[]
			
		item['upc'] = 0	
		item['availability'] = -3
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://b.scorecardresearch.com/p?c1=2&c2=8234779&cv=2.0&cj=1'
		item['siteID'] = 'bikedekho'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportReplacement'] = 30
		item['cities'] = []
		item['keyword'] = []
		item['minShippingDays'] = -1
		item['maxShippingDays'] = -1
		item['warrenty'] = -1
		
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