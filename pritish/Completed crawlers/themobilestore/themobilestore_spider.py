from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Themobilestore(CrawlSpider):
	name = "themobilestore"
	allowed_domains = ["www.themobilestore.in"]
	start_urls = [
		"http://www.themobilestore.in"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'themobilestore'
		
		toyield = 0
		try:
			name = hxs.select("//div[@id='title']/h1/text()").extract()[0].strip()
			
			item['name'] = name
			check = str(name)
			if len(check)!=0:
				toyield+=1
		except:
			item['name'] = ' ' 
			
		try:
			price = re.sub('\D','',re.sub('\.00','',str(hxs.select("//div[@class='our_price']//span/text()").extract())))
			item['price'] = int(price)
			if isinstance(item['price'],int)==1:
				toyield+=1
		except:
			item['price'] = 0
			
		try:
			rating = re.sub('\D','',re.sub('\.00','',str(hxs.select("//span[@id='rating1']/@rating").extract())))
			
			item['rating'] = int(rating)
		except:
			item['rating'] = -1
			
		try:
			avail = str(hxs.select("//span[@class='in-stock']/b/text()").extract())
			if avail.find("In Stock.")!=-1:
				item['availability'] = 1
		except:
			item['availability'] = -3
			
		try:
			deliv = re.sub('\s',' ',re.sub('\D',' ',str(hxs.select("//span[@class='ships-in']/b/text()").extract())))
			item['minShippingDays'] = int(deliv[3])
			item['maxShippingDays'] = int(deliv[7])
		except:
			item['minShippingDays'] = -1
			item['maxShippingDays'] = -1
			
			
		try:
			img = hxs.select("//a[@class='variant-image']/img/@src").extract()
	
			
			item['images'] = img
		except:
			item['images'] = []
			
		try:
			warranty = str(hxs.select("//div[@id='warranty']/text()").extract())
			war =  re.sub('\D',' ',str(hxs.select("//div[@id='warranty']/text()").extract()))
			if warranty.find("Years")!=-1 or warranty.find("Year")!=-1 or warranty.find("year")!=-1:
				war1 = int(war)*12
			if warranty.find("months")!=-1 or warranty.find("Months")!=-1:
				war1 = int(war)
			item['warrenty'] = war1
		except:
			item['warrenty'] = -1
			
		try:
			details = str(hxs.select("//div[@id='description']//p/text()").extract())
			details1 = re.sub('\s'," ",details)
			item['details'] = details1
		except:
			item['details'] = []
		try:
			sp = []
			sk = []
			specs = hxs.select("//div[@id='feature_groups']//td/text()").extract()
			for counter in specs:
				sp.append(counter)
			flag = 1
			for counter1 in sp:
				if flag%2==0:
					sk.append(counter1)
					flag+=1
				else:
					flag+=1
			sv = {}
			sv = dict(zip(sp,sk))		#The specs are alittle mismatched...I couldnt come up with either a logic or an XPath to split them
			item['specs'] = sv
		except:
			item['specs'] = []
			
		try:
			#name: StringList
			categories = hxs.select("//div[@id='browse-nodes']/a/text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>' and category.strip()!='&amp':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
		item['upc'] = 0
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://a01.buildabazaar.com/img/lookandfeel/31103/2e19ed541909556e27f03_999x350x.png.999xx.png'
		item['siteID'] = 'themobilestore'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]
		
		try:
			brand = name
			brand1 = str(name)
			brand2 = brand1.find(" ")
			brand3 = brand1[:brand2]
			item['brand'] = brand3			#Extracts the brand
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