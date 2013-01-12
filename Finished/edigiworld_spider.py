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
	name = "edigiworld"
	allowed_domains = ["www.edigiworld.com"]
	start_urls = [
		"http://www.edigiworld.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'edigiworld'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[@class='container9']/div[@class='ctl_aboutbrand']/h1/text()").extract()[0]
			#name: Integer
			item['price'] = hxs.select("//div[@class='productprices']/span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_spnMRP']/span[@class='mrp']/span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_lblMrp']/text()").extract()[0]
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='productlagreimg']/div[@id='bankImageDiv']/a[@id='zoomImg']/img[@id='bankImage']/@src").extract()
		except:
			item['images']=['wrong']
		
		try:
			#name: String
			item['shippingCost'] = hxs.select("//div[@class='productprices']/span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_spnWebPrice']/span[@class='offer']/span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_lblOfferPrice']/text()").extract()[0]
		except:
			item['shippingCost']=''
		try:
			#name: String
			item['brand'] = hxs.select("//div[@class='container9']/div[@class='ctl_aboutbrand']/div[@class='productbrand']/span[@class='brandlname']/text()").extract()[0]
		except:
			item['brand']=''
		try:
			#name: Float
			item['rating'] = hxs.select("//div[@id='ctl00_ContentPlaceHolder1_Ratings_ctl00_divReview']/div[@id='ctl00_ContentPlaceHolder1_Ratings_ctl00_divAvgRat']/text()").extract()[0]
		except:
			item['rating']=-1
		try:
			#name: StringList
			item['details']=hxs.select("//div[@class='productdetail_leftdiv']/div[@class='container22']/div[@id='tabs']/div[@id='Description']/p/text()").extract()
		except:
			item['details']=[]
		###########################################################################
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
