from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData
from scrapy.http import Request
from time import sleep 
import hashlib
import re

class Urbantouch(CrawlSpider):
	name = "urbantouch"
	allowed_domains = ["www.urbantouch.com","urbantouch.com"]
	start_urls = [
		"http://www.urbantouch.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: Strig
		item['siteName'] = 'ubtouch'
		toyield=1
		try:
			#name: String
			item['name'] = str(hxs.select("//div[@class='product-shop']/h1/text()").extract()[0]).strip()
			item['price']= int(re.sub('[A-Za-z.\s]','',hxs.select("//span[@class='oprice']/text()").extract()[0]))
		except:
			toyield=0
		try:
			#name: StringList (a table with all details of the product)
			cont=hxs.select("//*[@id='additional_information']/div/table").extract()
			count=1
			while (cont != '') :
				cont=hxs.select("//*[@id='additional_information']/div/table/tr["+str(count)+"]/td[1]/text()").extract()[0]
				if cont == "Brand" :
					item['brand']=hxs.select("//*[@id='additional_information']/div/table/tr["+str(count)+"]/td[2]/a/text()").extract()[0].strip()
				count=count+1
		except:
			item['brand']=""
		upc=''
		try:
			#name: StringList (a table with all details of the product)
			cont=hxs.select("//*[@id='additional_information']/div/table").extract()
			count=1
			while (cont != ''):
				cont=hxs.select("//*[@id='additional_information']/div/table/tr["+str(count)+"]/td[1]/text()").extract()[0].strip()
				if cont == "SKU ID":
					upc=hxs.select("//*[@id='additional_information']/div/table/tr["+str(count)+"]/td[2]/text()").extract()[0].strip()
				count=count+1
		except:
			item['upc']=upc

		#name: StringList (a table with all details of the product)
		cont=hxs.select("//*[@id='additional_information']/div/table/tr[2]/td[1]/text()").extract()
		count=1
		category={}
		try:
			while (cont != ''):
			
				cont=hxs.select("//*[@id='additional_information']/div/table/tr["+str(count)+"]/td[1]/text()").extract()[0].strip()
				if cont == "Category":
					categories=hxs.select("//*[@id='additional_information']/div/table/tr["+str(count)+"]/td[2]/span").extract()
					catcount=1;
					for cat in categories:
						withincat=hxs.select("//*[@id='additional_information']/div/table/tr["+str(count)+"]/td[2]//text()").extract()
						for subcat in withincat:
							subcat=subcat.strip()
							if subcat!='':
								category[subcat]=''
							catcount=catcount+1
				count=count+1
		except:
				item['category']=category.keys()
					
		
			
		
		try:
			description=hxs.select("//meta[@name='description']/@content").extract().strip()
		except:	
			description=['']
		try:
			details=hxs.select("//div[@id='product_details']/div/p/text()").extract().strip()
		except:	
			details=['']
		if len(details)==0:
			details=['']
		item['details']=details[0]+" "+description[0]
		try:
			specs=dict()
			count=1
			cont=hxs.select("//*[@id='product_details']/div[1]/table/tbody/tr[1]/td[1]").extract()
			while cont!='':
				specs[hxs.select("//*[@id='product_details']/div[1]/table/tbody/tr["+str(count)+"]/td[1]/text()").extract()[0]]=hxs.select("//*[@id='product_details']/div[1]/table/tbody/tr["+str(count)+"]/td[2]/text()").extract()[0].strip()
				count=count+1
		except:
			item['specs']=specs
		
			
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='thumbnail-images']/img/@src").extract()
		except:
			item['images']=[]
		try:
			#name: String (need tp go to /cart/count to find the count available)
			availability=hxs.select("//div[@class='product-shop']/p[@class='availability']/span/text()").extract()[0].strip()
			if(lower(str(availability))=='out of stock'):
				item['availability'] = -1
		except:
			item['availability']=-3

		
		try:
			item['barcode']=item['upc']
			item['productID']=item['identifier']
			item['upclist']=[]
			item['warrenty']=0
			item['shippingCost']=0
			item['siteName']='Urban Touch'
			item['siteLogo']=''
			item['siteID']='ubtouch'
			item['rating']=0
			item['supportEMIInstallment']=False
			item['supportCashOnDelivery']=True
			item['supportReplacement']=True
			item['minShippingDays']=-1
			item['maxShippingDays']=-1
			item['noOfReviews']=-1
			item['cities']=[]
		except:
			abc=1

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