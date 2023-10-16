from typing import Iterable
import scrapy
from scrapy.http import Request
from adscraper.items import ApartmentItem

class AdspiderSpider(scrapy.Spider):
    name = "adspider"
    allowed_domains = ["www.sreality.cz"]
    start_urls = ["https://www.sreality.cz/en/search/for-sale/apartments"]
    num_ads = 0
    last_page_visited = None
    item_limit = 500


    def start_requests(self):
        url = "https://www.sreality.cz/en/search/for-sale/apartments"
        yield scrapy.Request(url, meta={'playwright': True, 'download_timeout': 0})


    def parse(self, response):
        #print(f"EVO TEKST:{response.css('.dir-property-list span.basic span::text').get()}")
        apartments = response.css('.dir-property-list .property.ng-scope span.basic')
        base_url = 'https://www.sreality.cz/'
        #print(f"number of apartments:{len(apartments)}\napartments checked:{self.num_ads}")
        for apartment in apartments:
            self.num_ads += 1
            if self.num_ads > self.item_limit:
                break
            apartment_page = apartment.css('h2 a::attr(href)').get()
            """
            title = apartment.css('h2 a span::text').get()
            location = apartment.css('.locality.ng-binding::text').get()
            price = apartment.css('.price.ng-scope span::text').get()
            """
            apartment_page_url = base_url + apartment_page
            self.last_page_visited = apartment_page_url
            yield response.follow(apartment_page_url, callback=self.parse_apartment_page, meta={'playwright': True, 'download_timeout': 0})
        
        next_page = response.xpath("//ul[@class='paging-full']/li[@class='paging-item']/following-sibling::li[11]/a/@href").get()
        #print(f"naslednja stran:{next_page}")
        next_page_url = base_url + next_page
        if self.num_ads < self.item_limit:
            yield response.follow(next_page_url, callback=self.parse, meta={'playwright': True, 'download_timeout': 0})


    def parse_apartment_page(self, response):
        title1 = response.css('.property-title h1 span.name.ng-binding::text').get()
        #image1 = response.css('.ng-isolate-scope .ob-c-carousel__content img::attr(src)').get()
        image1 = response.css('.ob-c-carousel__content img::attr(src)').get()
        """
        yield {
            'title': title1,
            'image_url': image1,
            'page_url': self.last_page_visited
        }
        """
        apartment_item = ApartmentItem()
        apartment_item['title'] = title1
        apartment_item['image_url'] = image1
        yield apartment_item