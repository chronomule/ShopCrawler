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
	name = "compareindia"
	allowed_domains = ["naaptol.com"]
	start_urls = [
		"http://www.naaptol.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'naaptol.com'
		toyield=1
		try:
			item['name'] = hxs.select("//div[@class='productDetails']/h1").extract()
			#item['price'] = int(re.sub('\D','',re.sub('\.00','',hxs.select("//div[@class='pro_PriceInfo']/text()").extract()[1].encode("utf-8",'ignore'))))
		except:
			toyield = 0
		try:
			item['images'] = hxs.select("//a/img[@id='zoomImage']/@src").extract()
		except:
			item['images']=[]
		
		try:
			#name: StringList
			categories = hxs.select("//div[@class='bradCrumbDiv']/ul/span/a/span/text()").extract()
			if len(categories)==0:
				categories.extend(hxs.select("//div[@class='bradCrumbDiv']/ul//text()").extract())
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
		try:
			#name: Float
			item['rating'] = hxs.select("//div[@class='prodPromDesLayout']/div[@class='prodPromDesDiv'][2]").extract()
		except:
			item['rating']=-1
		det=''
		try:
			#name: StringList
			details =  hxs.select("//div[@id='product_Details']/text()").extract()
			for detail in details:
				det=det+" "+detail.strip()
			item['details']=det
		except:
			item['details']=det
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='prodPromDesDiv'][3]/div[@class='priceDiv']/h2/text()").extract()[0]
		except:
			item['discount']=[]
		try:
			#name: String
			item['upc']=hxs.select("//div[@class='prodPromDesLayout']/div[3]/p/text()").extract()[0]
		except:
			item['upc']=''
		try:
			item['brand']= hxs.select("//div[@class='productDetails']/div[@class='pro_RatingINfo']/ul/text()").extract()[0]
		except:
			item['brand'] = ''
		item['shippingCost'] = 'Free'
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://images.naptol.com/usr/local/csp/staticContent/images_layout/naaptol.gif'
		item['siteID'] = 'naaptol'
		item['supportEMIInstallment'] = True 
		item['supportCashOnDelivery'] = True   
		item['supportReplacement'] = 30
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
