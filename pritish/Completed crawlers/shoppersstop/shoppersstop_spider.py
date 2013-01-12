from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Shoppersstop(CrawlSpider):
	name = "shoppersstop"
	allowed_domains = ["www.shoppersstop.com"]
	start_urls = [
		"http://www.shoppersstop.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'shoppersstop'
		
		toyield = 0
		try:
			name = hxs.select("//span[@class=' font_bold ']/text()").extract()[0].strip()
			
			item['name'] = name
			check = str(name)
			if len(check)!=0:
				toyield+=1
		except:
			item['name'] = ' ' 
			
		try:
			price = re.sub('\D',"",re.sub('\.00',' ',str(hxs.select("//td[@class='reg_price_noSale_text font_bold over_underline ']/text()").extract())))
			item['price'] = int(price)
			if isinstance(item['price'],int)==1:
				toyield+=1
		except:
			item['price'] = 0
			
		try:
			#name: StringList
			categories = hxs.select("//div[@class='C4HeaderStyle4LT_C1R1']/a/text()").extract()
			cat=[]
			for category in categories:
				if category.strip()!='Home' and category.strip()!= '' and category.strip()!='&gt;' and category.strip()!='>' and category.strip()!='&amp':
					cat.append(category.strip())
			item['category']=cat
		except:
			item['category']=[]
			
		try:
			det = hxs.select("//table[@class='product_info_section']//span/text()").extract()
			flag=0
			for counter in det:
				if flag==0:
					a = counter
					flag+=1
			if str(a).find("Product Details")!=-1:
				item['details'] = []
			else:
			
				item['details'] = a
		except:
			item['details'] = ' '
			
		try:
			upc = str(hxs.select("//td[@class='item_value']/text()").extract())
			upc1 = re.sub(" ","",re.sub('\D',"",upc))
			item['upc'] = int(upc1)
		except:
			item['upc'] = 0
			
		try:
			cod = str(hxs.select("//td[@class='cod_text']/text()").extract())
			if cod.find("Cash on Delivery Available ")!=-1:
				item['supportCashOnDelivery'] = True
			else:
				item['supportCashOnDelivery'] = False
		except:
			item['supportCashOnDelivery'] = False
			
		try:
			ship = str(hxs.select("//div[@class='font_no_bold tab_text']/text()").extract())
			ship1 = ship.find("-")
			ship2 = ship[ship1-1]
			ship3 = ship[ship1+1]
			item['minShippingDays'] = int(ship2)
			item['maxShippingDays'] = int(ship3)
		except:
			item['minShippingDays'] = -1
			item['maxShippingDays'] = -1
			
		try:
			img = hxs.select("//td[@id='product_image']/img/@src").extract()
			item['images'] = img
		except:
			item['images'] = []
			
		try:
			ab = []
			specs = hxs.select("//ul[@class='prod_info_bullet']/li/text()").extract()
			for counter in specs:
				ab.append(counter)
			item['specs'] = ab
		except:
			item['spec'] = []
		try:
			for counter in ab:
				p = str(counter)
				if p.find("Warranty")!=-1:
					q = re.sub('\D',"",p)
					if p.find("Years")!=-1 or p.find("Year")!=-1 or p.find("year")!=-1 or p.find("years")!=-1:
						item['warrenty'] = int(q)*12
					elif p.find("Months")!=-1 or p.find("months")!=-1:
						item['warrenty'] = int(q)
		except:
			item['warrenty'] = -1
			
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] = hxs.select("//a[@href='http://www.shoppersstop.com/index.jsp.vr']/img/@src").extract()
		item['siteID'] = 'shoppersstop'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['cities']=[]
		item['keyword']=[]	
		item['availability'] = -1
		
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
			