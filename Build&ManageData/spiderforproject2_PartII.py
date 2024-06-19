# Import os => Library used to easily manipulate operating systems
## More info => https://docs.python.org/3/library/os.html
import os 

# Import logging => Library used for logs manipulation 
## More info => https://docs.python.org/3/library/logging.html
import logging

# Import scrapy and scrapy.crawler 
import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpiderPage(scrapy.Spider):

    # Name of your spider
    name = "booking"

    # Url to start your spider from the 2 first pages
    start_urls = ['https://www.booking.com/searchresults.es.html?ss=Marsella&ssne=Marsella&ssne_untouched=Marsella&label=es-fr-booking-desktop-   ZhDEzpPYijqKk0AauqIHWAS652829001322%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9055006%3Ali%3Adec%3Adm&aid=2311236&lang=es&sb=1&src_elem=sb&src=index&dest_id=-1449947&dest_type=city&checkin=2024-02-15&checkout=2024-02-16&group_adults=2&no_rooms=1&group_children=0',
                  'https://www.booking.com/searchresults.es.html?label=es-fr-booking-desktop-ZhDEzpPYijqKk0AauqIHWAS652829001322%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9055006%3Ali%3Adec%3Adm&aid=2311236&ss=Marsella&ssne=Marsella&ssne_untouched=Marsella&lang=es&sb=1&src_elem=sb&src=index&dest_id=-1449947&dest_type=city&checkin=2024-02-15&checkout=2024-02-16&group_adults=2&no_rooms=1&group_children=0&offset=25'                
    ] 

#/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div
    # Callback function that will be called when starting your spider
    # It will get text, author and tags of all <div> with class="quote"
    def parse(self, response):
        quotes = response.xpath('/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div')
        for quote in quotes:
            yield {                                                
                'hotel name': quote.xpath('div[1]/div/div[1]/div/div[1]/div/h3/a/div[2]/text()').get(),      
                'area': quote.xpath('div[1]/div/div[1]/div/div[2]/div/a/span/span[1]/text()').get(),  
                'note': quote.xpath('div[1]/div/div[2]/div/div/div/a/span/div/div[1]/text()').getall(),           
                'nb coments': quote.xpath('div[1]/div/div[2]/div/div/div/a/span/div/div[2]/div[2]/text()').getall(),     
                'price': quote.xpath('div[2]/div[2]/div/div[1]/span/text()').getall(),          
            }


# Name of the file where the results will be saved
filename = "Booking_hotels.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('src/'):
        os.remove('src/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'src/' + filename: {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(QuotesSpiderPage)
process.start()