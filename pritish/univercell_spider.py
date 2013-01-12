from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData 
from scrapy.http import Request
from time import sleep 
import re
import hashlib

class Univercell(CrawlSpider):
	name = "univercell"
	allowed_domains = ["www.univercell.in"]
	start_urls = [
		"http://www.univercell.in"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		item['url'] = response.url.split('?')[0]
		m = hashlib.md5()
		m.update(item['url'])
		item['identifier'] = m.hexdigest()
		#name: String
		item['siteName'] = 'univercell'
		
		try:
			name = hxs.select("//h2[@class='productpageHeading']/text()").extract()[0].strip()
			
			item['name'] = name
		except:
			item['name'] = ' ' 
		
		try:
			price = re.sub('\D','',re.sub('\.00','',str(hxs.select("//span[@class='regularPrice']/text()").extract())))
			item['price'] = int(price)
		except:
			item['price'] = 0
			
		try:
			img = hxs.select("//div[@class='prel']//a/@href").extract()
			img.extend(hxs.select("//a[@rel='example_group']/img/@src").extract())
			item['images'] = img
		except:
			item['images'] = []
			
		try :
			avail = str(hxs.select("//div[@class='boxhead newstyleheading']/span[@class='productavailableinfo']/text()").extract())
			avail1 = re.sub('\W',' ',avail)
			if avail1.find("This Product is available for purchase")!=-1:
				item['availability'] = 1
		except:
			item['availability'] = -3
			
		item['category'] = []
		
		try:
			specs = hxs.select("//table[@class='keyfeaturetable']/text()").extract()
			item['specs'] = specs
		except:
			item['specs'] = []
		item['upc'] = 0
		item['barcode']=item['upc']
		item['productID'] = item['identifier']
		item['siteLogo'] ='http://img5.flixcart.com/www/prod/images/flipkart_india-31804.png'
		item['siteID'] = 'dailyobjects'
		item['supportEMIInstallment'] = True #if total order is more then 4000
		item['supportCashOnDelivery'] = True   #update this to check if cash on delivery is available or not for that particular product - cash on delivery is not available for too costly products
		item['supportReplacement'] = 30
		item['cities']=[]
		item['keyword']=[]
		try:
			br = name = hxs.select("//h2[@class='productpageHeading']/text()").extract()[0].strip()
			br1 = br.find(" ")
			br2 = br.find("u'")
			br3 = br[br2+1:br1]
			item['brand'] = br3
		except:
			item['brand'] = ' ' 
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