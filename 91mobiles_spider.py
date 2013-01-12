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
	name = "91mobiles"
	allowed_domains = ["http://www.91mobiles.com","www.91mobiles.com"]
	start_urls = [
		"http://www.91mobiles.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = '91mobiles'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='head']/h1/text()").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//div[@class='pricetag1']").extract()
		except:
			toyield=0
		try:	
			#name: String
			item['warrenty']=hxs.select("//div[@id='specifications']/table[@class='fk-specs-type2'][11]//text()").extract()
		except:
			item['warrenty']=[]
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@id='mobMedImg0']/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: StringList
			categories = hxs.select("//div[@class='breadcrumbstext']/text()").extract()
			cat=[]
			catcount=1
			if category!='91mobiles.com' and catcount!=len(categories):
				cat.append(category.strip())
			if catcount==len(categories):
				item['brand']=category.strip()
			catcount=catcount+1
				
			item['category']=cat
		except:
			item['category']=[]
		try:
			#name: StringList
			details =  hxs.select("//div[@class='destext']/text()").extract()
		except:
			item['details']=''
		try:
			#name: String
			item['deliveryDays'] = hxs.select("//div[@class='stock-section lastUnit tmargin5']/div[@class='shipping-details']/text()").extract()
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['warrenty'] = hxs.select("//div[@id='specifications']/table[@class='fk-specs-type2'][11]//tr[2]/td[@class='specs-value']/text()").extract()
		except:
			item['warrenty']=''	
		try:
			#name: Integer
			item['shippingCost'] = hxs.select("//div[@id='fk-stock-info-id']").extact()
		except:
			item['shippingCost']=0
		try:
			#name: String
			outOfStock= hxs.select("//div[@class='stock-section lastUnit tmargin5']/div[@id='fk-stock-info-id']").extract()[0]
			if outOfStock=='In stock':
				item['availability'] =outofStock
			else:
				item['availability'] =-3
		except:
			item['availability'] = -3
		try:
			#name: String
			item['brand'] = hxs.select("//div[@class='line fk-lbreadbcrumb']/span[3]/a/span/text()").extract()
		except:
			item['brand']=''
		try:
			#name: Float
			ratings= int(re.sub("[\D]",'',hxs.select("//div[@class='phonetextpanel']//a[3]/img/@src/text()").extract()[0]))
			ratings=float((ratings-5)/100)
			if ratings!=0:
				item['rating'] =ratings
			else:
				item['rating'] =-1
		except:
			item['rating'] = -1
		try:
			#name: String
			item['delivery days']=hxs.select("//div[@class='shipping-details']").extract()
		except:
			item['deliveryDays']=''
		try:
			#name: String
			olscount=1
			ols=hxs.select("//div[@class='stock-section lastUnit tmargin5']")
			for ol in ols:
				ilscount=1
				if "delivery time" in hxs.select("//div[@class='stock-section lastUnit tmargin5']["+str(olscount)+"]/div[@class='shipping-details']").extract()[0].strip().lower():
					shippingdays=re.sub('[\D]',' ',hxs.select("//div[@class='stock-section lastUnit tmargin5']/["+str(olscount)+"]/div[@class='shipping-details']").extract()[0].strip()).split()
				olscount=olscount+1
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
			#name: String
			item['publisher']=hxs.select("//div[@id='details'][1]/table[@class='fk-specs-type1']//tr[@class='odd'][4]/td[@class='specs-value']/b/text()").extract()[0]
		except:
			item['publisher']=''
		try:
			#name: String
			item['artist']=hxs.select("//div[@id='details']/ul[@class='verticle_list']/li[@class='fk_list_darkgreybackground fks_list_darkgreybackground'][1]/div[@class='lastUnit product_details_values']").extract()
		except:
			item['artist']=''
		try:
			#name: String
			item['musicLabel'] = hxs.select("//li[@class='fk_list_darkgreybackground fks_list_darkgreybackground'][4]/text()").extract()
		except:
			item['musicLabel']=''
		try:
			#name: String
			item['manufacturer'] = ''
		except:
			item['manufacturer']=''
		try:
			#name:Integer
			item['upc'] = int(re.sub("[\D]",'',hxs.select("//tr[@class='odd'][2]").extract()))
		except:
			item['upc']=0
		try:
			#name: String
			item['discount'] = hxs.select("//div[@class='price-table']/div[@class='line'][2]/text()").extract()[0]
		except:
			item['discount']=''
		try:
			#name: String	
			item['actor']=hxs.select("//li[@class='fk_list_darkgreybackground fks_list_darkgreybackground'][1]").extract()
		except:
			item['actor']=''
		try:
			#name: String
			item['director']=hxs.select("//li[@class='fk_list_greybackground fks_list_greybackground'][1]/text()").extract()
		except:
			item['director']=''
		item['shippingCost'] = 0
		item['upc']=0
		item['upclist'] = []
		item['barcode']=0
		item['productID'] = item['identifier']
		item['siteLogo'] =''
		item['siteID'] = 'flipkart'
		item['supportEMIInstallment'] = True
		item['supportCashOnDelivery'] = True
		item['supportReplacement'] = 30
		item['cities']=[]
		item['specs']={}
		if toyield:
			yield item
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(self.start_urls[0]+url, callback=self.parse)
			except:
				print  "Unexpected error:"
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(url, callback=self.parse)
			except:
				print  "Unexpected error:"
		sleep(2)