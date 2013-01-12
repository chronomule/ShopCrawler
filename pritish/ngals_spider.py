from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Ngaloriginals(CrawlSpider):
	name = "ngaloriginals"
	allowed_domains = ["www.ngaloriginals.com"]
	start_urls = [
		"http://www.ngaloriginals.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'ngaloriginals'
		
		toyield=1
		try:
			#name: String
			name = hxs.select("//div[@class='top']/h1/text()").extract()[0].strip()
			   #Stores the name
			item['name']= name
			#name: Integer
		except:
			toyield=0
		try:
			price = re.sub('\D','',re.sub('\.00','',str(hxs.select("/html/body/div[2]/div/div[2]/div[2]/div[2]/text()").extract())))
		
			item['price'] = int(price)	#srch4 stores the price
			
		except:
			toyield=0
		
		try:
			upc = name4
			upc1 = name4.find(",")
			upc2 = name4[upc1+2:]
			upc3 = upc2.replace("'"," ")
			item['upc'] = upc3
		except:
			item['upc'] = 0
		item['rating'] = -1
		item['warrenty'] = -1
		images=[]
		try:
			images=hxs.select("//a[@class='fancybox']/img/@src").extract()
			#name: StringList
			
			item['images'] = images
		except:
			item['images']=[]
		try:
			#name: StringList
			categories = hxs.select("//div[@class='breadcrumb']//text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>':
					cat.append(category.strip())
			for counter in cat:
				stored = counter
				flag=0
				for counting in cat:
					if stored==counting:
						flag+=1
				if flag>1:
					cat.remove(stored)		#To remove duplication in the category list
			item['category']=cat
		except:
			item['category']=[]	
			
		det=''
		try:
			#name: StringList
			details =  str(hxs.select("//div[@id='tab-description']/div/text()").extract()).strip(" ")
			details1 = details.replace("\\r","")
			details2 = details1.replace("\\n","")
			details3 = details2.replace("\\t","")
			details4 = details3.replace("u'',","")
			details5 = details4.find(".',")
			details6 = details4[:details5]
			details7 = details6+"]"
			item['details']="".join(details7)
		except:
			item['details']=det			
		
		
		try:
			avail = hxs.select("//div[@id='stock_info']/text()").extract()
			avail1 = str(avail)
			if avail1.find("In Stock")!=-1:
				item['availability'] = 1
			else:
				item['availability'] = -1
		except:
			item['availability'] = -1
			
		try:
			sp=[]
			sp1 =[]
			sp2 =[]
			sp3 ={}
			specs = hxs.select("/html/body/div[2]/div[4]/table/tbody/tr/td/text()").extract()
			for counter in specs:
				sp.append(counter)
			flag=1
			for coup in sp:
				if flag%2==0:
					sp1.append(coup)
					flag+=1
				else:
					sp2.append(coup)
					flag+=1
			sp3 = dict(zip(sp2,sp1))		#Stores it all in a dictionary
			item['specs'] = sp3
		except:
			item['specs'] = []
			
		item['brand']=' '	
		
		item['shippingCost']=0
		item['minShippingDays']= -1
		item['maxShippingDays']= -1
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteID'] = 'dailyobjects'
		item['supportEMIInstallment'] = True #if total order is more then 4000
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