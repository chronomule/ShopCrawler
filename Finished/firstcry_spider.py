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
	name = "firstcry"
	allowed_domains = ["www.firstcry.com"]
	start_urls = [
		"http://www.firstcry.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = LetsBuy()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'firstcry'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//div[2]/h1[@id='ctl00_ContentPlaceHolder1_lbl_ProductName']/text()").extract()[0]
			#name: Integer
			item['price'] = re.sub('\D','',re.sub('\.00','',hxs.select("//div[@class='lbl_pricediv_css']/span[@id='ctl00_ContentPlaceHolder1_lbl_mrp']/text()").extract()[0].encode("utf-8",'ignore')))
		except:
			toyield=0
		try:
			#name: StringList
			item['images'] = hxs.select("//div[@class='small_img_box']/img[@id='ctl00_ContentPlaceHolder1_thmbImage1']/@src").extract()
		except:
			item['images']=['wrong']
		try:
			#name: String
			item['shippingCost'] = hxs.select("//div[@class='lbl_pricediv_css']/span[@id='ctl00_ContentPlaceHolder1_lbl_mrp']/text()").extract()[0]
		except:
			item['shippingCost']=''
		try:
			#name: String
			item['brand'] = hxs.select("//div[@id='ctl00_ContentPlaceHolder1_BrandBoxDiv']/img[@id='ctl00_ContentPlaceHolder1_imgBrand']/@src").extract()[0]
		except:
			item['brand']=''
		try:
			#name: Float
			item['rating'] = hxs.select("//div[@id='ctl00_ContentPlaceHolder1_InstRating']/a[@id='ctl00_ContentPlaceHolder1_InstRating_A']/span[@id='ctl00_ContentPlaceHolder1_InstRating_Star_5']").extract()
		except:
			item['rating']=-1
		try:
			#name: Integer
			item['upc']=hxs.select("//div[@class='lbl_shipping_css']/span[@id='disp_proid']/text()").extract()[0]
		except:
			item['upc']=0
		try:
			#name: StringList
			item['details']=hxs.select("//div[@id='ctl00_ContentPlaceHolder1_pnl_product_info']/text()").extract()
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
