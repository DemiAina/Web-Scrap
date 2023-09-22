import scrapy

class HouseScrap(scrapy.Spider):
    name = 'HouseScrap'
    start_urls = ['https://www.myhome.ie/rentals/cork/property-to-rent']

    # custom_settings = { 
    #     'DOWNLOAD_DELAY':5
    # }

    def parse(self, response):
        for houses in response.css('div.ng-star-inserted'):
            try:
                yield {
                    
                    'Price' :  houses.css('h2.card-title.my-4.fs-1::text').get(), 
                    'Location' : houses.css('h3.card-text.mt-4::text').get() , 
                    'Number of bed rooms' : houses.css('span.p-1.ng-star-inserted::text').get() ,
                    'link':'https://www.myhome.ie/' + houses.css('a.col-9').attrib['href'] ,
             }
            except: 
                yield {
                    
                    'Price' : 'No price', 
                    'Location' : houses.css('h3.card-text.mt-4::text').get() , 
                    'Number of bed rooms' : houses.css('span.p-1.ng-star-inserted::text').get() ,
                    'link':'No link',
             }


