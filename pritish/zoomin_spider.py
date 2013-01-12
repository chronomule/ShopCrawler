from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Zoomin(CrawlSpider):
	name = "zoomin"
	allowed_domains = ["camera.zoomin.com"]
	start_urls = [
		"http://camera.zoomin.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'zoomin'
		
		toyield=1
		try:
			#name: String
			name = hxs.select("//h1/text()").extract()
			name1 = str(name)
			name2 = name1[28:]
			name3 = name2.find("']")
			name4 = name2[1:name3]
			name5 = str(name4)
			name6= name5.replace(" '","u'")
			item['name']= name6
			#name: Integer
		except:
			toyield=0
		try:
			price = hxs.select("//span[@id='product-price-101']//text()").extract()[2]
			srch = ","
			srch1 = price.find(srch)
			srch2 = price[:srch1]
			srch3 = price[srch1+1:]
			srch4 = srch2+srch3
			item['price'] = int(srch4)		#srch4 stores the price
			
		except:
			toyield=0
		try:	
			#name: String
			warrenty=hxs.select("//div[@class='section-content last']/ul[@class='clearfix']/li//text()").extract()
			war = str(warrenty)
			if war.find("Years")!=-1:
				war1 = war.find("Years")
				war2 = war[war1-2]
				item['warrenty'] = int(war2)*12
			elif war.find("Months")!=-1:
				war1 = war.find("Months")
				war2 = war[war1-2]
				item['warrenty'] = int(war2)
		except:
			item['warrenty']=-1
		images=[]
		try:
			images=hxs.select("//div[@class='product-preview-image']/a/@href").extract()
			#name: StringList
			images.extend(hxs.select("//div[@class='product-preview-image']//a[@href='http://a.zi.cm/v18/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/2/_/2_1_3.jpg']/img/@src").extract())
			images.extend(hxs.select("//div[@class='product-preview-image']//a[@href='http://a.zi.cm/v18/media/catalog/product/cache/1/image/500x500/9df78eab33525d08d6e5fb8d27136e95/3/_/3_2_2.jpg']/img/@src").extract())
			
			item['images'] = images
		except:
			item['images']=images
		
		try:
			#name: StringList
			categories = hxs.select("//div[@class='breadcrumbs']//text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
		
		det=''
		try:
			#name: StringList
			details =  hxs.select("//div[@ id='product_tabs_description_contents']/p/text()").extract()
			item['details']="".join(details)
		except:
			item['details']=det			
		

		try:
			specleft = hxs.select("//table[@id='product-attribute-specs-table']//td[@class='label']//text()").extract()
			specright = hxs.select("//table[@id='product-attribute-specs-table']//td[@class='data']//text()").extract()
			specdict = {}
			specdict = dict(zip(specleft, specright)) #This line is used to create the dictionary
			item['specs'] = specdict		#specdict is the dictionary which contains the specs of the product
			
		except:
		
			item['specs'] = []
			
			
		item['brand']=' '	
		
		item['shippingCost']=0
		item['availability'] = -3
		try:
			#name: Float
			item['rating']= float(re.sub("[A-Za-z]",'',hxs.select("//div[@class='fk-stars']/@title").extract()[0]).strip())
		except:
			item['rating'] = -1
		
		item['minShippingDays']= -1
		item['maxShippingDays']= -1
		
		try:
			#name:Integer
			item['upc'] = int(re.sub("[\D]",'',hxs.select("//tr[@class='odd'][2]").extract()))
		except:
			item['upc']=0
			
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteID'] = 'dailyobjects'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]
		item['siteLogo'] ='http://camera.zoomin.com'
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
				
				
		yield item
		
		sleep(2)