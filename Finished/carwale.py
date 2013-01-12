from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData
from scrapy.http import Request
from scrapy.http import FormRequest
from time import sleep 
import hashlib
import re


class Carwale(CrawlSpider):
	name = "carwale"
	allowed_domains = ["www.carwale.com"]
	start_urls = [
		"http://www.carwale.com/research"
	]
	
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		
		m = hashlib.md5()
		m.update(response.url)
		toyield=True
		item = CrawlerData()
		items=[]
		##########################################################################
		if re.search("^(http://www.carwale.com/research/)(.*)(\-details\-)(.*)(.html)$",response.url)==None:
			toyield=False
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='left-grid']/h1[@class='hd1']/text()").extract()[0]
		except:
			item['name']=''
			toyield=False
		try:
			#price: Integer
			item['price'] = int(re.sub("[\D]","",hxs.select("//div[@id='divPricingNew']/p/span/strong/text()").extract()[0]))
		except:
			item['price']=0
			toyield=0
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		item['siteName'] = 'Car Wale'
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		item['minShippingDays']=-1
		item['maxShippingDays']=-1
		item['availability']=-3
		item['shippingCost'] = 0
		item['category']=[]
		item['upc']=0
		item['upclist'] = []
		item['upclist']=[]
		item['barcode']=''
		item['productID']=item['identifier']
		item['upclist']=[]
		item['siteLogo']='http://img.carwale.com/cw-common/logo.gif'
		item['siteID']='carwale'
		item['supportEMIInstallment']=False
		item['supportCashOnDelivery']=False
		item['supportCashOnDelivery']=False
		item['supportReplacement']=False
		item['cities']=[]
		item['details']=''
		try:
			#rating: String
			rating = hxs.select("//div[@id='crRating_divDetails']/img[@src]").extract()
			ratingfinal=0
			for rate in rating:
				if rate=='http://img.carwale.com/images/ratings/1.gif':
					ratingfinal=ratingfinal+1
				if rate=='http://img.carwale.com/images/ratings/half.gif':
					ratingfinal=ratingfinal+0.5
			ratingfinal=ratingfinal/5
			item['rating'] = ratingfinal
		except:
			item['rating']=-1
		try:
			item['brand']=hxs.select("//ul[@class='breadcrumb']/li[4]/a/text()").extract()[0]
		except:
			item['brand']=''

		'''
		item['specs']={}
		item['variants']={}
		item['images']=''
		'''
		try:
			item['noOfReviews']=int(re.sub("[\D]",'',hxs.select("//a[@class='reviewLink']/text()").extract()[0]))
		except:
			item['noOfReviews']=-1
		##########################################################################
		
		'''
		'images': [u'http://img.carwale.com/cars/2418b.jpg'],
		'rating': [u'http://img.carwale.com/images/ratings/half.gif'],
		'specs': {},
		'variants': {}}
		'''
		
		
		imageurl=hxs.select("//div[@class='car-desc-rt']/div[3]/a[@href]").extract()[0]
		Request("http://www.carwale.com"+imageurl,callback=lambda r:self.parseImages(item))	
		items.append(item)
		return items
			
		#except:
		#item['images']=[]
		#try:
		#specificationsurl=hxs.select("//ul[@class='tab-nav']/li[2]/a[@href]")
		#yield Request("http://www.carwale.com"+specificationsurl, callback=self.parseSpecifications)
		#except:
		#item['specs']={}
		#try:
		#featuresurl=hxs.select("//ul[@class='tab-nav']/li[3]/a[@href]")
		#yield Request("http://www.carwale.com"+featuresurl, callback=self.parseFeatures)
		#except:
		#abc=1
		#try:
		#coloursurl=hxs.select("//ul[@class='tab-nav']/li[4]/a[@href]")
		#yield Request("http://www.carwale.com"+coloursurl, callback=self.parseColours)
		#except:
		#item['variants']=[]
		#yield Carwale.item
		'''
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request("http://www.carwale.com"+url, callback=self.parse)
			except:
				print url
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(url, callback=self.parse)
			except:
				abc=1 
		#if toyield:
			#yield item
		'''
		sleep(2)
	#def parseFeatures(self, response):	print "Parse features"	hxs = HtmlXPathSelector(response)
	#def parseSpecifications(self, response):print "Parse specs" hxs = HtmlXPathSelector(response)
	#def parseColours(self, response):print "Parse colour" hxs = HtmlXPathSelector(response) colours=hxs.select("//table[@id='dlColors']/tr/td/div/div[2]/text()")	variants={}		count=0		for colour in colours:			variant['title']='Colour'			variant['order']=count			variant['text']=re.sub("[\t]",'',colour.strip())			variants.append(variant)			count=count+1		item['variants']=variants		#yield Carwala.item
	
	def parseImages(self, response,item):
		hxs = HtmlXPathSelector(response)
		images= hxs.select("//div[@id='thumbRow101']/table/tr/td/a/@href").extract()
		item['images']=images
		print "parseimages"
		return item
		#= hxs.select("//div[@id='thumbRow101']/table/tr/td/a/@href").extract()
		#item['images'] = hxs.select("//div[@id='thumbRow101']/table/tr/td/a/@href").extract()
	
