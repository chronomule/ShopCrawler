from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector 
from crawler.items import CrawlerData
from scrapy.http import Request
from time import sleep 
import re
import hashlib
class homeshop18(CrawlSpider):
	name = "homeshop18"
	allowed_domains = ["www.homeshop18.com"]
	start_urls = [
		"http://www.homeshop18.com"
	]
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		item = CrawlerData()
		m = hashlib.md5()
		m.update(response.url)
		item['identifier'] = m.hexdigest()
		item['url'] = response.url
		#name: String
		item['siteName'] = 'HomeShop 18'
		toyield=1
		###########################################################################
		try:
			#name: String
			item['name'] = hxs.select("//*[@class='pdp_title_section']/h1[@id='productLayoutForm:pbiName']/text()").extract()[0]
			#name: Integer
			item['price'] = int(re.sub('\D','',re.sub('\.00','',hxs.select("//span[@id='productLayoutForm:OurPrice']/text()").extract()[0].encode("utf-8",'ignore'))))
		except:
			toyield=0
		try:
			images=hxs.select("//div[@class='moreViews']/ul/li/a/img/@src").extract()
			item['images']=images
		except:
			item['images']=[]
		if len(item['images'])==0:
			item['images']=hxs.select("//img[@itemprop='image']/@src").extract()
		try:
			#name: String
			shippingdays=re.sub('\D',' ', hxs.select("//div[@class='pdp_details_deliveryTime']/text()").extract()[0].strip()).strip().split()
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
			#name: Integer
			availability=re.sub("[\W]","",hxs.select("//div[@class='pdp_details_block ']/table[@class='productShippingInfo']//tr[2]/td/span/text()").extract()[0])
			if availability=="In Stock":
				item['availability']=-3
			if availability=="Pre Order":
				item['availability']=-2
			if availability=="Out of Stock":
				item['availability']=-1
		except:
			item['availability']=-3
			#dont rely on the availibility genrated here for some products the availibility is fetched from the server
			#/faces/servlet/PILServlet1?param=key+","+menuval1+","+catalogueId;
		try:
			#name: String
			warrenty=hxs.select("//div[@class='pdp_details_block ']/table[@class='productShippingInfo']//tr[1]/td/text()").extract()[0]
			if "month" in warrenty.lower() and "year" in warrenty.lower():
				x=-1
			if "month" in warrenty.lower():
				x=1
			if "year" in warrenty.lower():
				x=12
			item['warrenty'] = x*int(re.sub("[\D]","",hxs.select("//div[@class='pdp_details_block ']/table[@class='productShippingInfo']//tr[1]/td/text()").extract()[0]))
		except:
			item['warrenty']=-1
		item['shippingCost'] = 0
		'''
		try:
			#name: String
			item['brand'] = hxs.select("//div[@class='product_dscrpt_summarytxt_box']/div[@id='specifications']/table[@class='specs_txt'][1]//tr[1]/td[@class='specs_value']").extract()[0]
		except:
			item['brand']=''
		'''
		try:
			#name: StringList
			breadcrumb=hxs.select("//h4[@class='breadcrumbs']//a/text()").extract() 
			catlist=[]
			for category in breadcrumb:
				if(str(category).strip() != 'HomeShop18'):
					catlist.append(category.strip())
			item['category'] =  catlist
		except:
			item['category']=catlist
		try:
			#name: Float
			ratings=hxs.select("//span[@class='reviewSummary_ratingStarCount']/text()").extract()
			rat=0
			noofratings=0
			count=0;
			for rating in ratings:
				rat=rat+(int(re.sub("[\D]",'',rating))*(5-count))
				count=count+1
				noofratings=noofratings+int(re.sub("[\D]",'',rating))
			if(len(ratings)!=0):
				rat=rat/noofratings
			else:
				rat=-1
			item['rating']=rat
		except:
			item['rating']=-1
		try:
			#name: String
			
			details=hxs.select("//table[@class='specs_txt'][1]/tbody/tr")
			count=0;
			brand=''
			for detail in details:
				count=count+1
				try:
					if('brand' in hxs.select("//table[@class='specs_txt'][1]/tbody/tr["+str(count)+"]/td[1]/text()").extract()[0].strip().lower()):
						brand=hxs.select("//table[@class='specs_txt'][1]/tbody/tr["+str(count)+"]/td[2]/a/text()").extract()[0].strip()
						item['brand']=brand
					count=count+1
				except:
					abc=1
			item['brand']=brand
		except:
			item['brand']=''
		
		try:
			upc=hxs.select("//div[@class='pdp_details_sku']/span/text()").extract()
			item['upc']=re.sub("[\D]","",hxs.select("//div[@class='pdp_details_sku']/span/text()").extract()[0])
			'''
			rows1=hxs.select("//div[@class='pdp_title_section']/div[@class='pdp_details_sku']/span/text()").extract()
			rows2=hxs.select("//table[@class='productKeywords']//td[2]/text()").extract()
			'''
		except:
			item['upc']=upc
		'''
		#name: Integer
		i=0
		for r in rows1:
			if(rows1[i]=='ISBN'):
				item['upc'] = rows2[i]
				break;
			i=i+1
		except:
			item['upc']=0
		'''
		try:
			#name: IntegerList
			item['upclist'] = []
		except:
			item['upclist']=[]
		'''
		try:
			#name: String
			item['publisher']=hxs.select("//table[@class='productKeywords']//text()").extract()[0]
		except:
			item['publisher']=''
		'''
		details=''
		'''
		try:
			#name: StringList
			
			details=hxs.select("//div[@class='product_dscrpt_summarytxt_box']//text()").extract()[0]
			
		except:
			details=''
		'''
		try:
			#name: StringList
			description=hxs.select("//div[@id='specifications']/p[1]/text()").extract()[0]
		except:
			description=''
		item['details']=details+description
		
		specs={}
		try:
			specifications=hxs.select("//div[@id='specifications']//table").extract()
		except:
			abc=1
		count=1
		for table in specifications:
			#check if table has a header
			try:
				header=hxs.select("//div[@id='specifications']//table["+str(count)+"]/tbody/tr[1]/th/text()").extract()[0]
			except:
				header=''
			rows=hxs.select("//div[@id='specifications']//table["+str(count)+"]/tbody/tr").extract()
			rowcount=1
			for row in rows:
				addtospecs=True
				try:
					text=hxs.select("//div[@id='specifications']//table["+str(count)+"]/tbody/tr["+str(rowcount)+"]/td[2]/text()").extract()[0]
					title=header+" "+hxs.select("//div[@id='specifications']//table["+str(count)+"]/tbody/tr["+str(rowcount)+"]/td[1]/text()").extract()[0]
				except:
					try:
						text=hxs.select("//div[@id='specifications']//table["+str(count)+"]/tbody/tr["+str(rowcount)+"]/td[1]/text()").extract()[0]
						title=header
					except:
						addtospecs=False
				
						
				if(addtospecs):
					specs[title]=text
				rowcount=rowcount+1
			count=count+1

			
		item['specs']=specs
		item['barcode']=item['upc']
		item['productID']=item['identifier']
		item['upclist']=[]
		item['shippingCost']=0
		item['siteName']='Home Shop 18'
		item['siteLogo']='http://www.homeshop18.com/homeshop18/media/images/homeshop18_2011/header/hs18-logo.png'
		item['siteID']='homeshop18'
		item['supportEMIInstallment']=False
		try:
			cod=hxs.select("//div[@id='pdp_details_cod']").extract()
			if(cod==''):
				item['supportCashOnDelivery']=False
			else:
				item['supportCashOnDelivery']=True
		except:
			item['supportCashOnDelivery']=False
		item['supportCashOnDelivery']=True
		item['supportReplacement']=True
		try:
			noOfReviews=hxs.select("//div[@class='pdp_details_review_count']/a/text()").extract()[0]
			item['noOfReviews']=int(re.sub("[\D]",'',noOfReviews))
		except:
			item['noOfReviews']=-1
		item['cities']=['Agra','Ahmedabad','Ahmednagar','Ajmer','Akola','Aligarh','Allahabad','Alwar','Ambala','Amravati','Amritsar','Anand','Ananthpur','Angul','Ankleswar','Anpara','Asansol','Aurangabad','Baddi','Bahadurgarh','Bahraich','Balasore','Bangalore','Bareilly','Baroda','Basti','Begusarai','Behrampur','Belgaum','Bellary','Berhampur','Bhagalpur','Bharuch','Bhatinda','Bhavnagar','Bhilwara','Bhiwadi','Bhopal','Bhubaneshwar','Bijapur','Bikaner','Bilaspur','Billimora','Bokaro','Calicut','Chandigarh','Chennai','Chiplun','Chittoor','Cochin','Coimbatore','Cuttack','Daman','Darbhanga','Davangere','Dehra Dun','Delhi','Dewas','Dhanbad','Dharwad','Dibrugarh','Dimapur','Dombivali','Durg','Ernakulam','Etah','Etawah','Faizabad','Faridabad','Farokkabad','Fatehabad','Firozabad','Gadag','Gandhi Nagar','Gandhidham','Gaya','Ghaziabad','Ghazipur','Giridih','Goa','Godhra','Gorakhpur','Gulbarga','Guna','Guntur','Gurgaon','Guwahati','Gwalior','Haldia','Haldwani','Haridwar','Hasan','Hathras','Hissar','Hoshiarpur','Hospet','Hosur(TN','Howrah','Hubli','Hyderabad','Ichalakaranchi','Imphal','Indore','Jabalpur','Jagadhalpur','Jagadhri','Jaipur','Jalgaon','Jallandhur','Jalna','Jammu','Jamnagar','Jamshedpur','Jaunpur','Jhansi','Jharsugda','Jodhpur','Jorhat','Junagadh','Kadi','Kakinada','Kalol(Dt-Mehsana)','Kalyan','Kannur','Kanpur','Karad','Karnal','Kashipur','Katihar','Katni','Khanna','Kharagpur','Kharar','Kolhapur','Kolkatta','Korba','Kota','Kottayam','Kurnool','Kurukshetra','Lakhimpur Kheri','Lucknow','Ludhiana','Madurai','Malda','Mandi','Mandigovindgarh','Manesar','Mangalore','Manipal','Mathura','Meerut','Mehsana','Midnapur Town','Mirzapur','Moga','Mohali','Moradabad','Morbi','Mumbai','Munger','Muzzafarpur','Muzzaffarnagar','Mysore','Nadiad','Nagpur','Nallasopara','Namakkal','Nanded','Nashik','Navsari','Nellore','New Delhi','Noida','Palakkad','Pali','Panchkula','Panipet','Panjim','Paradeep','Pathankot','Patiala','Patna','Phagawara','Pondicherry','Porbander','Port Blair','Pune','Puri','Purnea','Raibarely','Raigarh','Raipur','Rajamundry','Rajkot','Rajpura','Rampur','Ranchi','Ratnagiri','Renukut','Rewa','Rohtak','Roorkee','Rourkela','Rudrapur','Sagar','Saharanpur','Salem','Samastipur','Sambalpur','Sangli','Sangrur','Satara','Satna','Secenderabad','Shahjahanpur','Shimla','Shimoga','Sholapur','Silchar','Silvassa','Sirsa','Sitapur','Solan','Sonepat','Sriganga Nagar','Srikakulam','Sultanpur','Surat','Surendranagar','Tarapur','Thane','Tirupathi','Tiruppur','Trichur','Trichy','Trivandrum','Udaipur','Ujjain','Ulhas Nagar','Vadodara','Valsad','Vapi','Varanasi','Vellore','Vijayanagaram','Vijayawada','Visakapatanam','Warangal','Zirakpur']

		'''

		###########################################################################
		'''

			#item['name'] = re.sub('[^ a-zA-Z0-9]',' ',item['name']).strip()
			#item['deliveryDays']=re.sub('[^ a-zA-Z0-9]',' ',item['deliveryDays']).strip()
			#item['warrenty']=re.sub('[^ a-zA-Z0-9]',' ',item['warrenty']).strip()
			#item['shippingCost']=re.sub('[^ a-zA-Z0-9]',' ',item['shippingCost']).strip()
			#item['brand']=re.sub('[^ a-zA-Z0-9]',' ',item['brand']).strip()
			#item['manufacturer']=re.sub('[^ a-zA-Z0-9]',' ',item['manufacturer']).strip()
			#item['discount']=re.sub('[^ a-zA-Z0-9]',' ',item['discount']).strip()
			#item['publisher']=re.sub('[^ a-zA-Z0-9]',' ',item['publisher']).strip()
			#item['upclist']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['upclist'] ]
			#item['details']=[re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['details'] ]
			#item['category']=[ re.sub('[^ a-zA-Z0-9]',' ',u).strip() for u in item['category']]
			
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
		if toyield:
			yield item