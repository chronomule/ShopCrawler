from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class egully(CrawlSpider):
	name = "egully12"
	allowed_domains = ["http://www.egully.com","www.egully.com"]
	start_urls = [
		"http://www.egully.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'egully.com'
		toyield=1
		try:
			#name: String
			item['name'] = hxs.select("//div[@id='LayoutColumn2']/div[@id='ProductDetails']/div[@class='BlockContent']/h1/text()").extract()[0]
			#name: Integer
			item['price'] = int(re.sub('\D','',re.sub('\.00','',hxs.select("//div[@class='DetailRow'][2]/div[@class='Value']/em[@class='ProductPrice VariationProductPrice']/h2/b/text()").extract()[0].encode("utf-8",'ignore'))))
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='ProductThumbImage']/a/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: StringList
			categories = hxs.select("//div[@id='ProductBreadcrumb']/ul/span/a/span/text()").extract()
			if len(categories)==0:
				categories.extend(hxs.select("//div[@id='ProductBreadcrumb']/ul//text()").extract())
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
		try:
			#name: String
			deliveryDays=re.sub("[\D]"," ",hxs.select("//div[@class='ProductDetailsGrid']/div[@class='DetailRow'][7]/div[@class='Value']/text()").extract()[0])
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
			item['shippingCost'] = hxs.select("//div[@class='DetailRow'][2]/div[@class='Value']/em[@class='ProductPrice VariationProductPrice']/h2/b/text()").extract()[0]
		except:
			item['shippingCost']=''
		try:
			#name: String
			item['brand'] = hxs.select("//div[@class='DetailRow'][3]/div[@class='Value']/text()").extract()[0]
		except:
			item['brand']=''
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='ProductDetailsGrid']/div[@class='DetailRow'][2]/div[@class='Value']/span[@class='YouSave']/text()").extract()[1]
		except:
			item['discount']=''
		try:
			#name: String
			item['details']=hxs.select("//div[@id='ProductDescription']/div[@class='ProductDescriptionContainer']/div[@class='line description item_desc_text'][3]/text()").extract()[0]
		except:
			item['details']=[]
		item['shippingCost'] = 'Free'
	#	item['barcode'] = item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://www.egully.com/product_images/egullyLogo.png'
		item['siteID'] = 'Egully'
		item['supportEMIInstallment'] = False #if total order is more then 4000
		item['supportCashOnDelivery'] = True  #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = False
		item['cities']=[]
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
