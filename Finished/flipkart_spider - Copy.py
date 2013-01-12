from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
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
		item = LetsBuy()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'flipkart'
		toyield=1
		try:	
			#name: String
			item['name'] = hxs.select("//div[@class='mprod-summary-title fksk-mprod-summary-title']/h1/text()").extract()[0]
			#name: Integer
			item['price']=hxs.select("//div[@class='price-table']/div[@class='line']/span[@id='fk-mprod-our-id']/text()").extract()
		except:
			toyield=0
		try:	
			#name: String
			item['warrenty']=hxs.select("//div[@id='specifications']/table[@class='fk-specs-type2'][11]/tbody/text()").extract()
		except:
			item['warrenty']=[]
		try:
			#name: StringList		
			item['images'] = hxs.select("//div[@class='line bpadding10']//img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: StringList
	#		detailsarray = hxs.select("//span[@id='fk-mprod-our-id']/text()").extract()
	#		
	#		for word in detailsarray:
	#			item['price'] = item['price']+word
	#		
	#		detailsarray=hxs.select("//div[@id='description']/div[@class='item_desc_text line']/text()").extract()
			item['details']=hxs.select("//div[@id='description']/div[@id='description_text']").extract()
	#		for word in detailsarray:
	#			item['details'] = item['details']+word
		except:
			item['details']=[]
		try:
			#name: String
			item['deliveryDays'] = hxs.select("//div[@class='shipping-details']/span[@class='boldtext']/text()").extract()
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['warrenty'] = hxs.select("//div[@id='specifications']/table[@class='fk-specs-type2'][11]/tbody/tr[2]/td[@class='specs-value']/text()").extract()
		except:
			item['warrenty']=''	
		try:
			#name: Integer
			item['shippingCost'] = hxs.select("//div[@id='fk-stock-info-id']").extact()
		except:
			item['shippingCost']=0
		try:
			#name: String
			item['availability'] = hxs.select("//div[@id='fk-stock-info-id']").extact()
		except:
			item['availability']=-1
		try:
			#name: String
			item['brand'] = hxs.select("//div[@class='line fk-lbreadbcrumb']/span[3]/a/span/text()").extract()
		except:
			item['brand']=''
		try:
			#name: Float
			item['rating'] = hxs.select("//div[@class='fk-stars']/@title/text()").extract()[0]
		except:
			item['rating']=-1
		try:
			#name: String
			item['delivery days']=hxs.select("//div[@class='shipping-details']").extract()
		except:
			item['deliveryDays']=''
		try:
			#name: String
			item['publisher']=hxs.select("//div[@id='details'][1]/table[@class='fk-specs-type1']//tr[@class='odd'][4]/td[@class='specs-value']/b/text()").extract()[0]
		except:
			item['publisher']=''
		try:
			#name: String
			item['artist']=hxs.select("//div[@id='details']/ul[@class='verticle_list']/li[@class='fk_list_darkgreybackground fks_list_darkgreybackground'][1]/div[@class='lastUnit product_details_values']").extract()
		except:
			item['artist']=''
		try:
			#name: String
			item['musicLabel'] = hxs.select("//li[@class='fk_list_darkgreybackground fks_list_darkgreybackground'][4]/text()").extract()
		except:
			item['musicLabel']=''
		try:
			#name: String
			item['manufacturer'] = ''
		except:
			item['manufacturer']=''
		try:
			#name:Integer
			item['upc'] = hxs.select("//div[@id='details'][1]//table[@class='fk-specs-type1']//tr[@class='odd'][2]").extract()[0]
		except:
			item['upc']=0
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='price-table']/div[@class='line'][2]//text()").extract()
		except:
			item['discount']=''
		try:
			#name: String	
			item['actor']=hxs.select("//li[@class='fk_list_darkgreybackground fks_list_darkgreybackground'][1]").extract()
		except:
			item['actor']=''
		try:
			#name: String
			item['director']=hxs.select("//li[@class='fk_list_greybackground fks_list_greybackground'][1]/text()").extract()
		except:
			item['director']=''
		if toyield:
			#item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
			#item['deliveryDays']=re.sub('[^ a-zA-Z0-9]',' ',item['deliveryDays']).strip()
			#item['warrenty']=re.sub('[^ a-zA-Z0-9]',' ',item['warrenty']).strip()
			#item['brand']=re.sub('[^ a-zA-Z0-9]',' ',item['brand']).strip()
			#item['manufacturer']=re.sub('[^ a-zA-Z0-9]',' ',item['manufacturer']).strip()
			#item['discount']=re.sub('[^ a-zA-Z0-9]',' ',item['discount']).strip()
			#item['publisher']=re.sub('[^ a-zA-Z0-9]',' ',item['publisher']).strip()
			#item['upclist']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['upclist'] ]
			#item['details']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['details'] ]
			#item['category']=[ re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['category']]
			#item['author'] = re.sub('[^ a-zA-Z0-9]',' ',item['author']).strip()
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
		#except:
		#	print "Unexpected error:"
		#	yield item
		
