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
	name = "tradus"
	allowed_domains = ["www.tradus.in"]
	start_urls = [
		"http://www.tradus.in"
	]
	def parse(self, response):
		'''
		rating = Field()
		noOfReviews=Field()
		productID=Field()
		category=Field()
		sites=Field()
		
		
		
		
		
		price=Field()
		availability = Field()
		deliveryDays = Field()
		siteName=Field()
		siteLogo=Field()
		siteID=Field()
		minShippingDays=Field()
		maxShippingDays=Field()

		'''
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'tradus'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@id='left-content-product-details-part1']/h1[@class='left-content-product-heading']/text()").extract()
			#name: String
			item['price'] = int(re.sub('\D','',re.sub('\.00','',hxs.select("//b[@id='tPrice']/text()").extract()[0])))
		except:
			toyield=0
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@class='product_image_bg']/table//tr/td[1]/ul/li/a[@class='cloud-zoom-gallery']/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: Float
			item['rating']=hxs.select("//div[@id='seller_review_block']/text()").extract()[0]
		except:
			item['rating']=''
		#det=''
		try:
			#name: StringList
			item['details'] = hxs.select("//div[@id='product-information']/p[3]/text()").extract()[0]		
			
		except:
			item['details'] = []
			
		try:
			item['availability'] = hxs.select("//div[@id='left-content-product-details-price-left']/div[@id='QtyAlarm']/text()").extract()[0]
		except:
			item['availability']=''
		try:
			#name: String
			item['publisher']=hxs.select("//div[@id='product-specification']/table[5]//tr/td[@id='product-spec']/p/text()").extract()[0]
		except:
			item['publisher']=''
		try:
			#name: Integer
			item['upc'] = hxs.select("//div[@id='product-specification']/table[4]//tr/td[@id='product-spec']/p").extract()[0]
		except:
			item['upc']=0
		item['shippingCost'] = 'Free Shipping'
		specs={}
		upclist=[]
		try:
			#name:Integer
			tables=hxs.select("//div[@id='product-specification']/table[1]")
			tablescomputers=hxs.select("//div[@id='product-specification']")
			tableothers=hxs.select("//div[@id='product-specification']/table[1]")
			tables.extend(tablescomputers)
			if len(tables)==0:
				tables.extend(tableothers)
			for table in tables:
				rows=table.select("tr")
				for row in rows:
					try:
						key=row.select("td[@id='product-value']/text()").extract()[0].strip()
					except:
						try:
							key=row.select("td[@id='product-spec']/p/text()").extract()[0].strip()
						except:
							try:
								key=row.select("td[@id='product-spec']/text()").extract()[0].strip()
							except:
								try:
									keyas=row.select("td[1]//text()").extract()
									for keya in keyas:
										if keya.strip()!='':
											key=keya
										else:
											key=''
								except:
									key=''
					try:
						val=row.select("//td[@id='product-spec']//text()").extract()[0]
					except:
						val=row.select("td//text()").extract()[0]
						val=''
					key=re.sub(":","",key)
					if key!='' and val!='':
						specs[key]=val
					if key=="ISBN":
						item['upc']=val
					if "ISBN" in key:
						upclist.extend(val.split(','))
			item['upclist']=upclist
			item['specs']=specs
			item['upclist']=upclist
			item['brand']=brand		
			item['specs']=specs
		except:
			item['specs']=specs
		try:
			#name: StringList
			categories = hxs.select("//div[@id='full-main-content-center']/div[@id='breadcrump']/span/a/span/text()").extract()
			if len(categories)==0:
				categories.extend(hxs.select("//div[@id='full-main-content-center']/div[@id='breadcrump']//text()").extract())
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=''
		item['barcode']=0
		item['productID']=item['identifier']
		item['siteLogo']='http://static.tradus.ibcdn.com/sites/all/themes/basic/images/ci_images/tradus_logo3.png'
		item['siteID']='tradus'
		item['supportEMIInstallment']=True
		item['supportCashOnDelivery']=False
		item['supportReplacement'] = False
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