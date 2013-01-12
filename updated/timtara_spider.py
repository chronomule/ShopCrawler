from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class homeshop18(CrawlSpider):
	name = "timtara"
	allowed_domains = ["http://www.timtara.com","www.timtara.com"]
	start_urls = [
		"http://www.timtara.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'timtara'
		toyield=1
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='textgray'][1]/span[@class='textblackbold']/text()").extract()[0]
			#name: Integer
			item['price'] = re.sub('\D','',re.sub('\.00','',hxs.select("//div[@class='Value']/em[@class='ProductPrice VariationProductPrice']/b/text()").extract()[0].encode("utf-8",'ignore')))
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='ProductTinyImageList']/ul/li[@id='TinyImageBox_0']/div/a/img[@id='TinyImage_0']/@src").extract()
		except:
			item['images']=['wrong']
		det=''
		try:
			#name: StringList
			details =  hxs.select("//div[@class='ProductDescriptionContainer textgray']/text()").extract()[0]
			for detail in details:
				det=det+" "+detail.strip()
			item['details']=det
		except:
			item['details']=det
		try:
			#name: StringList
			categories = hxs.select("//div[@id='ProductBreadcrumb']/span/a/span/text()").extract()
			if len(categories)==0:
				categories.extend(hxs.select("//div[@id='ProductBreadcrumb']//text()").extract())
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
		try:
			#name: String
			item['warrenty'] = hxs.select("//div[@class='ProductDetailsGrid textgray']/div[@class='DetailRow'][4]/div[@class='Value']/text()").extract()[0]
		except:
			item['warrenty']=''
		try:
			#name: String
			item['brand'] = hxs.select("//div[@class='ProductDetailsGrid textgray']/div[@class='DetailRow'][3]/div[@class='Value']/a/text()").extract()[0]
		except:
			item['brand']=''
		try:
			#name: String
			item['upc'] = re.sub('\D','',re.sub('\.00','',hxs.select("//div[@class='ProductDetailsGrid textgray']/div[@class='DetailRow'][5]/div[@class='Value']/text()").extract()[0].encode("utf-8",'ignore')))
		except:
			item['upc']=0
		try:
			#name: String
			deliveryDays=re.sub("[\D]"," ",hxs.select("//div[@class='pro-deliver']").extract()[0])
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
			#name: String
			item['discount']=hxs.select("//div[@class='ProductDetailsGrid ProductAddToCart']/div[2]/div[3]/div[@class='relativ'][1]/div[@class='buybiggray']/text()").extract()[0]
		except:
			item['discount']=''
		try:
			#name: String
			item['publisher']=hxs.select("//table[@class='productKeywords']/text()").extract()[0]
		except:
			item['publisher']=''
		item['shippingCost'] = 'Free'
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://image1.timtara.com/product_images/logo.jpg'
		item['siteID'] = 'timtara'
		item['supportEMIInstallment'] = False #if total order is more then 4000
		item['supportCashOnDelivery'] = False  #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = False
		item['cities']=[]
		#item['brand']=''
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