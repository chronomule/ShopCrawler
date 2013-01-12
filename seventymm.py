from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Flipkart(CrawlSpider):
	name = "seventymm"
	allowed_domains = ["www.seventymm.com","shop.seventymm.com"]
	start_urls = [
		"http://shop.seventymm.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'seventymm'
		
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='ITitle']/h1/text()").extract()[0].strip()
			#name: Integer
			item['price'] = hxs.select("//label[@id='ctl00_cph_lblPrice']/span[@class='ISelPr']/text()").extract()
			#update to remove the instant cashback
		except:
			toyield=0
		try:	
			#name: String
			item['warrenty']=round(float(re.sub("[\D]"," ",hxs.select("//tr[3]/td[@class='PT10 PL10 DGryTxt']/text()").extract()[0]).strip().split(' ')[0])*12)
		except:
			item['warrenty']=-1
		#images=[]
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='IImgM']/div[@class='IImg']/img/@src").extract()
		except:
			item['images'] = []
		try:
			#name: StringList
			item['category'] = hxs.select("//div[@id='ctl00_divNav']/div[@class='GryTxt']/span/a/span/text()").extract()
			if len(categories)==0:
				categories = hxs.select("//div[@id='ctl00_divNav']/div[@class='GryTxt']/span/a/text()").extract()
			if len(categories)==0:
				categories.extend(hxs.select("//div[@id='ctl00_divNav']/div[@class='GryTxt']//text()").extract())
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
		#det=''
		try:
			#name: StringList
			details =  hxs.select("//div[@id='ctl00_cph_tab1']/div[@class='I_IDesc']/p[1]/text()").extract()
			item['details']="".join(details)
		except:
			item['details']=det
		item['shippingCost']=0
		try:
			#name: String
			instock=hxs.select("//table[@class='IDataTbl'][1]//tr[1]").extract()
			#outofstock = hxs.select("//div[@class='shipping-details']/span/text()").extract()[0]
			if instock=='In Stock.':
				item['availability'] =-3
			if instock=='Available.':
				item['availability'] =-3
			if instock=='Imported Edition.':
				item['availability'] =-3
			if outofstock=='Out of Stock':
				item['availability'] =-1
		except:
			item['availability'] = -4
		try:
			#name: Float
			item['rating']= float(re.sub("[A-Za-z]",'',hxs.select("//div[@class='fk-stars']/@title").extract()[0]).strip())
		except:
			item['rating'] = -1
		try:
			#name: String
			deliveryDays=re.sub("[\D]"," ",hxs.select("//*[@class='shipping-details']/span/text()").extract()[0])
			shippingdays=deliveryDays.strip().split(' ')
			if(int(shippingdays[0])<int(shippingdays[1])):
				item['minShippingDays'] = int(shippingdays[0])
				item['maxShippingDays'] = int(shippingdays[1])
			else:
				item['minShippingDays'] = int(shippingdays[1])
				item['maxShippingDays'] = int(shippingdays[0])
			
		except:
			
			item['minShippingDays']=-1
			item['maxShippingDays']=-1
		try:
			#name:Integer
			item['upc'] = int(re.sub("[\D]",'',hxs.select("//tr[@class='odd'][2]").extract()))
		except:
			item['upc']=0
		
		specs={}
		upclist=[]
		item['shippingCost'] = 0
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] =''
		item['siteID'] = 'seventymm'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 7
		item['cities']=[]
		item['keyword']=[]

		if toyield:
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