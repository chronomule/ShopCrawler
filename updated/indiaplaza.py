from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class indiaplaza(CrawlSpider):
	name = "indiaplaza"
	allowed_domains = ["www.indiaplaza.com","indiaplaza.com"]
	start_urls = [
		"http://www.indiaplaza.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		m = hashlib.md5()
		m.update(response.url)
		item['url'] = response.url
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'indiaplaza'
		toyield=1
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='fdpSkuArea']//h1/text()").extract()[0]
			#name: Integer
			item['price'] = int(re.sub('\D','',hxs.select("//span[@id='ContentPlaceHolder1_FinalControlValuesHolder_ctl00_FDPMainSection_lblOurPrice']/text()").extract()[0].encode("utf-8",'ignore')))
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='clearfix demo']//@src").extract()
		except:
			item['images']=['wrong']
		det=''
		try:
			#name: StringList
			details =  hxs.select("//div[@id='litDesc']/text()").extract()
			for detail in details:
				det=det+" "+detail.strip()
			item['details']=det
		except:
			item['details']=det
		try:
			#name: String
			item['deliveryDays'] = hxs.select("//span[@class='delDateQuest']/text()").extract()[0]
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='fdpSave']/text()").extract()[0]
		except:
			item['discount']=''
		try:
			#name: String
			item['warrenty'] = hxs.select("//div[@class='warrantyBg']/text()").extract()[0]
		except:
			item['warrenty']=''
		try:
			#name: Float
			item['rating']= float(re.sub("[A-Za-z]",'',hxs.select("//div[@class='ratingstar rstar37']").extract()[0]).strip())
		except:
			item['rating'] = -1
		try:
			#name: String
			item['brand']= hxs.select("//div[@class='specColr'][1]/div[@class='specMidLine']/div[@class='fdpSpecCol2r'][1]/text()").extract()[0]
		except:
			item['brand'] = ''
		try:
			#name: String
			item['publisher']= hxs.select("//div[@class='bksfdpltrArea']/ul/li[1]/span[@class='greyFont']/text()").extract()[0]
		except:
			item['publisher']=''
		try:
			#name: String
			item['upc'] = int(re.sub('\D','',hxs.select("//div[@class='bksfdpltrArea']/ul/li[2]/span[@class='greyFont']/h2/text()").extract()[0].encode("utf-8",'ignore')))
		except:
			item['upc']=''
		try:
			#name: StringList
			categories = hxs.select("//div[@id='virtualPath']/span/a/span/text()").extract()
			if len(categories)==0:
				categories.extend(hxs.select("//div[@id='virtualPath']//text()").extract())
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
		item['shippingCost'] = 'Free Shipping'
		item['manufacturer'] = ''
		item['availability'] = ''
		item['upclist'] = ''
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://images.indiaplaza.com/indiaplazaimages/logo.png'
		item['siteID'] = 'indiaplaza'
		item['supportEMIInstallment'] = False #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = False
		item['cities']=[]
		item['brand']=''
		if toyield:	
			item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
			item['deliveryDays']=re.sub('[^ a-zA-Z0-9]',' ',item['deliveryDays']).strip()
			item['warrenty']=re.sub('[^ a-zA-Z0-9]',' ',item['warrenty']).strip()
			item['shippingCost']=re.sub('[^ a-zA-Z0-9]',' ',item['shippingCost']).strip()
			item['brand']=re.sub('[^ a-zA-Z0-9]',' ',item['brand']).strip()
			item['manufacturer']=re.sub('[^ a-zA-Z0-9]',' ',item['manufacturer']).strip()
			item['discount']=re.sub('[^ a-zA-Z0-9]',' ',item['discount']).strip()
			item['publisher']=re.sub('[^ a-zA-Z0-9]',' ',item['publisher']).strip()
			item['upclist']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['upclist'] ]
			item['details']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['details'] ]
			item['category']=[ re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['category']]
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



	
