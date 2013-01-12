from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Watchkart(CrawlSpider):
	name = "watchkart"
	allowed_domains = ["www.watchkart.com"]
	start_urls = [
		"http://www.watchkart.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'watchkart'
		
		toyield=0
		try:
			#name: String
			name = hxs.select("//span[@class='product-name']/text()").extract()[0].strip()
			item['name'] = name
			check = str(name)
			if len(check)!=0:
				toyield+=1
			#name: Integer
		except:
			toyield=0
		try:
			price = str(hxs.select("//span[@class='spcl-price']/text()").extract())
			price1 = price.replace("\\u20a8. ","")
			price2 = price1.replace("[u'","")
			price3 = price2.replace("']","")
			price4 = price3.replace(".00","")
			price5 = price4.replace(",","")
				
			item['price'] = int(price5)	#srch4 stores the price
			if isinstance(item['price'],int)==1:
				toyield+=1
		except:
			toyield=0
		
		try:
			images=hxs.select("//a[@ id='MagicZoomPlusImagemagictoolbox1']/img/@src").extract()
			#name: StringList
			img1 = hxs.select("//a[@class='MagicThumb-swap']/img/@src").extract()
			if img1!=images:
				images.extend(hxs.select("//a[@class='MagicThumb-swap']/img/@src").extract())
			item['images'] = images
		except:
			item['images']=[]
		try:
			cod = str(hxs.select("//span[@class='top-free']/text()").extract())
			if cod.find("Cash On Delivery")!=-1:
				item['supportCashOnDelivery'] = True
		except:
			item['supportCashOnDelivery'] = False
			
		try:
			if cod.find("Free delivery in india")!=-1:
				item['shippingCost'] = 0
		except:
			item['shippingCost'] = -1
			
		try:
			#name: StringList
			categories = hxs.select("//ul[@class='breadcrumbs']//li//text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>' and category.strip()!='/':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
		try:
			ship = str(hxs.select("//span[@class='free-deliv']//span[@class='bottom-free']/text()").extract())
			ship1 = ship.find("-")
			ship2 = ship[ship1-2]
			ship3 = ship[ship1+2]
			item['minShippingDays'] = int(ship2)
			item['maxShippingDays'] = int(ship3)
		except:
			item['minShippingDays'] = -1
			item['maxShippingDays'] = -1
			
		try:
			specs = hxs.select("//span[@class='short-description']/p/text()").extract()
			flag = 0
			for counter in specs:
				item['details'] = counter
				if flag==0:
					break
		except:
			item['details'] = []
			
		try:
			sp = []
			ar = []
			pr = {}
			kr = []
			po = []
			kp = []
			spec = str(hxs.select("//span[@class='short-description']/p/text()").extract())
			sp1 = spec.replace("\xa0","")
			sp2 = sp1.replace("\\xa0","")
			for counter in sp2.split(","):
				ar.append(counter)
			flag = 0
			for counter in ar:
				if flag>=1:
					if counter[1]=="u":
						pr.append(counter)		#pr isthe list which contains the right side of the specs list
				flag+=1
			specright = str(hxs.select("//table[@id='product-attribute-specs-table']//td/text()").extract())
			a = specright.replace("u'\xa0',","")
			b = a.replace("u'\\xa0',","")
			c = b.replace(":","")
			d = c.replace('\\n',"")
			e = d.replace(" ","")
			flag = 2
			for counter in e.split(","):
				kr.append(counter)
			for counter1 in kr:
				if flag%2==0:
					sp.append(counter1)
					flag+=1
				else:
					ar.append(counter1)
					flag+=1
			du = 0
			for counter3 in ar:
				if du>=1:
					counter4 = counter3.replace("']","'")
					po.append(counter4)
					du+=1
				elif du<1:
					du+=1
			for counter5 in sp:
				counter6 = counter5.replace("[u'","u'")
				kp.append(counter6)
			pr = dict(zip(kp,po))
			item['specs'] = pr #This dictionary stores the speclist
		except:
			item['specs'] = []
			
		try:
			item['brand'] = pr["u'BrandName'"]
		except:
			item['brand'] = ' '
		try:
			item['upc'] = f["  u'Model No '"]
		except:
			item['upc'] = 0
			
		item['availability'] = -3
		item['rating'] = -1
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://s.dkrt.in/skin/frontend/default/helloone_wat/images/logo.png'
		item['siteID'] = 'watchkart'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportReplacement'] = 30
		item['cities'] = []
		item['keyword'] = []
		
		
		if toyield==2:
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
				
		
				
		
		
		sleep(2)