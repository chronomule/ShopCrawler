from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import LetsBuy 
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class homeshop18(CrawlSpider):
	name = "saholic"
	allowed_domains = ["www.saholic.com"]
	start_urls = [
		"http://www.saholic.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'saholic'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='product-main-title']/div[@class='name']/span[@class='product-name']/text()").extract()[0]
			#name: Integer
			item['price'] = re.sub('\D','',re.sub('\.00','',hxs.select("//div[@class='price']/span[@id='mrp']/text()").extract()[0].encode("utf-8",'ignore')))
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@id='vtab-media-img-1']/div[@class='container']/div[@class='slides']/div/img/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['deliveryDays'] =hxs.select("//div[@class='estimate left']/div[@id='shipping_time']").extract()[0] 
		except:
			item['deliveryDays']=''
		try:
			#name: Integer
			item['availability'] = hxs.select("//div[@class='pdp_details_block ']/table[@class='productShippingInfo']//tr[2]/text()").extract()[0]
		except:
			item['availability']=-1
		try:
			#name: String
			item['warrenty'] = hxs.select("//div[@class='warranty']/label[@class='bold']/text()").extract()[0]
		except:
			item['warrenty']=''
		try:
			#name: String
			item['brand'] = hxs.select("//div[@class='product-main-title']/div[@class='name']/span[@class='brand']").extract()[0]
		except:
			item['brand']=''
		try:
			#name: StringList
			item['category'] =  hxs.select("//h4[@class='breadcrumbs']//a/text()").extract() 
		except:
			item['category']=[]
		try:
			#name: Float
			item['rating'] = hxs.select("//span[@class='product_rating_5']/text()").extract()[0]
		except:
			item['rating']=-1
	
		try:
			#name: String
			item['manufacturer'] = hxs.select("//table[@class='specs_txt'][1]//tr[4]/text()").extract()[0]
		except:
			item['manufacturer']=''
		
		try:
			rows1=hxs.select("//div[@class='pdp_title_section']/div[@class='pdp_details_sku']/span/text()").extract()
			rows2=hxs.select("//table[@class='productKeywords']//td[2]/text()").extract()
			#name: Integer
			i=0
			for r in rows1:
				if(rows1[i]=='ISBN'):
					item['upc'] = rows2[i]
					break;
				i=i+1
		except:
			item['upc']=0
		try:
			#name: IntegerList
			item['upclist'] = []
		except:
			item['upclist']=[]
		try:
			#name: String
			item['discount']=hxs.select("//div[@class='price']/span[@class='price-diff']").extract()[0]
		except:
			item['discount']=''
		try:
			#name: String
			item['publisher']=hxs.select("//table[@class='productKeywords']//text()").extract()[0]
		except:
			item['publisher']=''
		try:
			#name: StringList
			item['details']=hxs.select("//div[@id='vtab-130001']/div[@class='desc']/ul/li[@class='introduction']/text()").extract()
		except:
			item['details']=[]
		###########################################################################
		if toyield:
			item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
			item['deliveryDays']=re.sub('[^ a-zA-Z0-9]',' ',item['deliveryDays']).strip()
			item['warrenty']=re.sub('[^ a-zA-Z0-9]',' ',item['warrenty']).strip()
			#item['shippingCost']=re.sub('[^ a-zA-Z0-9]',' ',item['shippingCost']).strip()
			item['brand']=re.sub('[^ a-zA-Z0-9]',' ',item['brand']).strip()
			item['manufacturer']=re.sub('[^ a-zA-Z0-9]',' ',item['manufacturer']).strip()
			item['discount']=re.sub('[^ a-zA-Z0-9]',' ',item['discount']).strip()
			item['publisher']=re.sub('[^ a-zA-Z0-9]',' ',item['publisher']).strip()
			item['upclist']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['upclist'] ]
			item['details']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['details'] ]
			item['category']=[ re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['category']]
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
