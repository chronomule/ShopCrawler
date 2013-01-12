from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class YeBhiSpider(CrawlSpider):
	name = "YeBhiSpider"
	allowed_domains = ["yebhi.com"]
	start_urls = [
		"http://www.yebhi.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'yebhi'
		toyield=1
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='product-desc']/text()").extract()[0]
			#name: Integer
			item['price'] = int(re.sub('\D','',re.sub('\.00','',hxs.select("//span[@class='price-offer']").extract()[0])))
		except:
			toyield=0
		try:
			#name: StringList
			item['images']=hxs.select("//div[@class='product-thumbnail']/a/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: Integer
			item['availability']= str(re.sub('[^ a-zA-Z0-9]','',hxs.select("//div[@class='product-instock']/text()").extract()[0]))
		except:
			item['availability']= -1
		try:
			#name: String
			item['brand']=hxs.select("//div[@class='middle-content-bg']/div[2]/div[1]/a/img/@src").extract()
		except:
			item['brand']=' '
		try:
			#name: String
			item['upc']=hxs.select("//div[@class='middle-content-bg']/div[2]/div[1]/div[@class='product-code']/text()").extract()
		except:
			item['upc']=''
		specs={}
		upclist=[]
		try:
			#name:Integer
			tables=hxs.select("//div[@id='tabDiv1']")
			tablesbooks=hxs.select("//table[@class='fk-specs-type1']")
			tableothers=hxs.select("//div[@id='tabDiv1']")
			tables.extend(tablesbooks)
			if len(tables)==0:
				tables.extend(tableothers)
			for table in tables:
				rows=table.select("tr")
				for row in rows:
					try:
						key=row.select("//div[@id='tabDiv1']//td[1]/text()").extract()[0].strip()
					except:
						try:
							key=row.select("//div[@id='tabDiv1']//td[1]/text()").extract()[0].strip()
						except:
							try:
								key=row.select("//div[@id='tabDiv1']//td[1]/text()").extract()[0].strip()
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
						val=row.select("//div[@id='tabDiv1']//td[2]//text()").extract()[0]
					except:
						val=row.select("td[2]//text()").extract()[0]
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
		item['shippingCost'] = 'Free'
		item['barcode'] = item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='/template/yebhi/images/yebhi.com_logo.jpg'
		item['siteID'] = 'yebhi'
		item['supportEMIInstallment'] = False #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = '30days'
		item['cities']=[]
		if toyield:
			item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
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