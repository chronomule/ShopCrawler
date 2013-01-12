from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class letsbuy(CrawlSpider):
	name = "letsbuy"
	allowed_domains = ["www.letsbuy.com"]
	start_urls = [
		"http://www.letsbuy.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'Lets Buy'
		toyield=1
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='top_content']/h1[@class='prod_name']/text()").extract()[0]
			#name: Integer
			item['price'] = float(re.sub("[\D]","",hxs.select("//div[@class='prod_summary']//div[@class='sub_list']//span[@class='offer_price']/text()").extract()[0]))/100
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//span[@class='image nodisplay']/text()").extract()
		except:
			try:
				item['images']=hxs.select("//img[@class='productMainImage']").extract()
			except:
				item['images']=[]
		try:
			#name: StringList
			categories = hxs.select("//p[@class='breadcrumb']/a[@class='headerNavigation']/text()").extract()
			cat=[]
			catcount=1
			for category in categories:
				if category!='Letsbuy.com' and catcount!=len(categories):
					cat.append(category.strip())
				if catcount==len(categories):
					item['brand']=category.strip()
				catcount=catcount+1
				
			item['category']=cat
		except:
			item['category']=[]
			item['brand']=''
		try:
			#name: StringList
			details =  hxs.select("//div[@id='product-overview']//text()").extract()
			det=''
			for detail in details:
				if detail.strip()!='':
					det=det+" "+detail.strip()
			item['details']=det
		except:
			item['details']=''
		try:
			#name: String
			olscount=1
			ols=hxs.select("//div[@class='sub_list']/ol")
			for ol in ols:
				ilscount=1
				if "delivery time" in hxs.select("//div[@class='sub_list']/ol["+str(olscount)+"]/li[1]").extract()[0].strip().lower():
					shippingdays=re.sub('[\D]',' ',hxs.select("//div[@class='sub_list']/ol["+str(olscount)+"]/li[3]").extract()[0].strip()).split()
				olscount=olscount+1
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
			olscount=1
			ols=hxs.select("//div[@class='sub_list']/ol")
			for ol in ols:
				ilscount=1
				if hxs.select("//div[@class='sub_list']/ol["+str(olscount)+"]/li[1]").extract()[0].strip()=="Warranty":
					warranty=re.sub('[\D]',' ',hxs.select("//div[@class='sub_list']/ol["+str(olscount)+"]/li[3]").extract()[0].strip())
					if "month" in warrenty.lower() and "year" in warrenty.lower():
						x=-1
					if "month" in warrenty.lower():
						x=1
					if "year" in warrenty.lower():
						x=12
					item['warrenty'] = x*int(re.sub("[\D]","",hxs.select("//div[@class='pdp_details_block ']/table[@class='productShippingInfo']//tr[1]/td/text()").extract()[0]))
		except:
			item['warrenty']=-1
		
		try:
			#name: Float
			outOfStock= hxs.select("//div[@class='btn_area out-of-stock']//img/@src").extract()[0]
			if outOfStock=='http://static1.lsbimg.com/images/coming-soon.jpg':
				item['availability'] =-4
			if outOfStock=='http://static1.lsbimg.com/images/out_of_stock_new.png':
				item['availability'] =-1
			else:
				item['availability'] =-3
		except:
			item['availability'] = -3

			
		try:
			#name: Float
			ratings= int(re.sub("[\D]",'',hxs.select("//div[@class='BVRRRatingNormalImage']/img/@alt").extract()[0]))
			ratings=float((ratings-5)/100)
			if ratings!=0:
				item['rating'] =ratings
			else:
				item['rating'] =-1
		except:
			item['rating'] = -1
			
		try:
			#name: Float
			noOfreviews= int(re.sub("[\D]",'',hxs.select("//span[@class='BVRRNumber']/img[@alt]").extract()[0]))
			item['noOfReviews'] =noOfreviews
		except:
			item['noOfReviews'] = 0

		item['shippingCost'] = 0
		item['upc']=0
		item['upclist'] = []
		item['barcode']=0
		item['productID']=item['identifier']
		item['siteLogo']='http://static1.lsbimg.com/images/letsbuy_logo.png'
		item['siteID']='letsbuy'
		item['supportEMIInstallment']=True
		item['supportCashOnDelivery']=True
		item['supportReplacement']=45
		item['cities']=[]
		item['specs']={}

		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(self.start_urls[0]+url,callback=self.parse)
			except:
				print "Item Unexpected error:"
		for url in hxs.select('//a/@href').extract():
			try:
				yield Request(url, callback=self.parse)
			except:
				print "Unexpected error:"
		if toyield:
			yield item
		sleep(2)
