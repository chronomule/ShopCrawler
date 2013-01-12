from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import hashlib
import re
class Next(CrawlSpider):
	name = "next"
	allowed_domains = ["www.next.co.in","next.com"]
	start_urls = [
		"http://www.next.co.in"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'next.co.in'
		toyield=1
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='ctl_aboutbrand']/h1/text()").extract()[0]
			#name: Integer	
			item['shippingCost']= float(re.sub("[\D]","",hxs.select("//span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_spnWebPrice']").extract()))
		except:		
			toyield=0
		try:
			#name: StringList		
			item['images'] = hxs.select("//img[@id='bankImage']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['deliveryDays']=hxs.select("//div[@class='leftpane']/img/@src").extract()
		except:
			item['deliveryDays']=''
		try:
			#name: StringList
			item['details'] = hxs.select("//div[@class='ctl_aboutproduct']/p[@class='product_desc']/text()").extract()
		except:
			item['details']=[]
		try:
			#name: Float
			ratings= int(re.sub("[\D]",'',hxs.select("//div[@id='ctl00_ContentPlaceHolder1_Ratings_ctl00_divAvgRat']").extract()[0]))
			ratings=float((ratings-5)/100)
			if ratings!=0:
				item['rating'] =ratings
			else:
				item['rating'] =-1
		except:
			item['rating'] = -1
		try:
			#name: StringList
			categories = hxs.select("//div[@id='ctl00_ContentPlaceHolder1_Breadcrum_ctl00_brdCrumbNormal']/text()").extract()
			cat=[]
			catcount=1
				if category!='flipkart.com' and catcount!=len(categories):
					cat.append(category.strip())
				if catcount==len(categories):
					item['brand']=category.strip()
				catcount=catcount+1
				
			item['category']=cat
		except:
			item['category']=[]
		item['availability'] = -1
		item['upclist'] = ''
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
			item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
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
