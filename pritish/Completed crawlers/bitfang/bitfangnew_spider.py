from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Bitfang(CrawlSpider):
	name = "bitfang"
	allowed_domains = ["www.bitfang.com"]
	start_urls = [
		"http://www.bitfang.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'bitfang'
		
		toyield = 0
		try:
			name = hxs.select("//div[@class='prodDetailsPname']/h1/text()").extract()[0].strip()
			
			item['name'] = name
			check = str(name)
			if len(check)!=0:
				toyield+=1
		except:
			item['name'] = ' ' 
			
		try:
			price = re.sub(" ","",re.sub('\D',' ',str(hxs.select("//span[@class='price-txt']/text()").extract())))
			item['price'] = int(price)
			if isinstance(item['price'],int)==1:
				toyield+=1
		except:
			item['price'] = 0
			
		try:
			#name: StringList
			categories = hxs.select("//ul[@class='paging1']//a/text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>' and category.strip()!='&amp':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
		try:
			img = hxs.select("//div[@class='ProdDetailsLeftWrap']/img/@src").extract()
			img.extend(hxs.select("//a[@class='highslide']/img/@src").extract())
			item['images'] = img
		except:
			item['images'] = []
			
		try:
			det = str(hxs.select("//div[@class='prodDetailsOverview']/text()").extract())		
			det1 = det.replace('\n',"")
			det2 = det1.replace('\\n',"")
			det3 = det2.replace('\\r',"")
			det4 = det3.replace("u\'","")		#This part can be modified. I couldnt come up with a regular expression which could remove all the odd spacing properly
			det5 = det4.replace("\'","")
			det6 = det5.replace("\\u","")
			det7 = det6.replace("       ","")
			item['details'] = det7
		except:
			item['details'] = []
			
		try:
			specleft = hxs.select("//tr[@class='whitebg']/td/text()").extract()
			a = []
			b = []
			flag = 2
			for counter in specleft:
				if flag%2==0:
					a.append(counter)
					flag+=1
				else:
					b.append(counter)
					flag+=1
			c = {}
			c = dict(zip(a,b))
			item['specs'] = c
		except:
			item['specs'] = []
			
		try:
			brand = str(name)
			brand1 = brand.find(" ")
			brand2 = brand[:brand1]
			item['brand'] = brand2
		except:
			item['brand'] = ' '
			
		try:
			war = str(c['Parts'])
			war1 = re.sub('\D',"",war)
			if war.find("Years")!=-1 or war.find("Year")!=-1 or war.find("year")!=-1:
				war2 = int(war1)*12
			if war.find("Months")!=-1 or war.find("months")!=-1:
				war2 = int(war1)
			item['warrenty'] = war2
		except:
			item['warrenty'] = -1
			
		item['upc'] = 0
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] = hxs.select("//a[@href='/Default.aspx']/img/@src").extract()
		item['siteID'] = 'bitfang'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportCashOnDelivery'] = False  #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]	
		item['minShippingDays'] = -1
		item['maxShippingDays'] = -1
		item['availability'] = -1
		
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