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
	name = "flipkart"
	allowed_domains = ["www.flipkart.com"]
	start_urls = [
		"http://www.flipkart.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'Flip Kart'
		
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='mprod-summary-title fksk-mprod-summary-title']/h1/text()").extract()[0].strip()
			#name: Integer
			item['price'] = int(re.sub('\D','',re.sub('\.00','',hxs.select("//span[@id='fk-mprod-our-id']/text()").extract()[1].encode("utf-8",'ignore'))))
			#update to remove the instant cashback
		except:
			toyield=0
		try:	
			#name: String
			item['warrenty']=round(float(re.sub("[\D]"," ",hxs.select("//div[@class='mprod-warrenty']/text()").extract()[0]).strip().split(' ')[0])*12)
		except:
			item['warrenty']=-1
		images=[]
		try:
			images=hxs.select("//div[@class='pp-image-carousel pp-carousel-short']//img/@src").extract()
			#name: StringList
			images.extend(hxs.select("//div[@id='mprodimg-id']/img/@src").extract())
			images.extend(hxs.select("//div[@class='image-wrapper']/img/@src").extract())
			
			item['images'] = images
		except:
			item['images']=images
		try:
			#name: StringList
			categories = hxs.select("//div[@class='line fk-lbreadbcrumb']/span/a/span/text()").extract()
			if len(categories)==0:
				categories.extend(hxs.select("//div[@class='line fk-lbreadbcrumb']//text()").extract())
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
		det=''
		try:
			#name: StringList
			details =  hxs.select("//div[@class='item_desc_text description']/p/text()").extract()
			for detail in details:
				det=det+" "+detail.strip()
			item['details']=det
		except:
			item['details']=det
		item['shippingCost']=0
		try:
			#name: String
			instock=hxs.select("//div[@class='stock-section lastUnit tmargin5']/div[@id='fk-stock-info-id']/text()").extract()[0]
			outofstock = hxs.select("//div[@class='shipping-details']/span/text()").extract()[0]
			if instock=='In Stock.':
				item['availability'] =-3
			if instock=='Available.':
				item['availability'] =-3
			if instock=='Imported Edition.':
				item['availability'] =-3
			if outofstock=='Out of Stock':
				item['availability'] =-1
		except:
			item['availability'] = -3
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
		try:
			#name:Integer
			tables=hxs.select("//table[@class='fk-specs-type2']")
			tablesbooks=hxs.select("//table[@class='fk-specs-type1']")
			tableothers=hxs.select("//div[@id='specifications']//table")
			tables.extend(tablesbooks)
			if len(tables)==0:
				tables.extend(tableothers)
			for table in tables:
				rows=table.select("tr")
				for row in rows:
					try:
						key=row.select("th[@class='specs-key']/text()").extract()[0].strip()
					except:
						try:
							key=row.select("td[@class='specs-key boldtext']/text()").extract()[0].strip()
						except:
							try:
								key=row.select("td[@class='specs-key']/text()").extract()[0].strip()
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
						val=row.select("td[@class='specs-value']//text()").extract()[0]
					except:
						try:
							val=row.select("td//text()").extract()[0]
						except:
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
		except:
			item['specs']=specs
		
		item['shippingCost'] = 0
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://img5.flixcart.com/www/prod/images/flipkart_india-31804.png'
		item['siteID'] = 'flipkart'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['brand']=''
		item['keyword']=[]
		
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
		
		if toyield:
			yield item
		
		sleep(2)