import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess


class BBBSpider(scrapy.Spider):
    name = 'bbb_spider'

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Read category URLs from file
        with open('input/category.txt', 'r') as file:
            category_urls = [url.strip().lower().replace(' ', '-') for url in file.readlines()]

        # Read country data from Excel
        country_data = pd.read_excel('input/country.xlsx', usecols=['Country', 'State', 'Business', 'State Name'])

        # Iterate over country data and category URLs
        for _, row in country_data.iterrows():
            country, state, business, state_name = row['Country'], row['State'], row['Business'], row['State Name']
            for category_url in category_urls:
                url = f"https://www.bbb.org/{country}/{business}/category/{category_url}"
                yield scrapy.Request(url, headers=headers, callback=self.parse, meta={'state': state_name, 'url.txt': url})

    def parse(self, response):
        state = response.meta['state']
        url = response.meta['url.txt']
        total = response.css('div.business-search-header h1 strong::text').get(default='Not Load')

        yield {'State': state, 'URL': url, 'Total': total}


# Run the spider
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'xlsx',
    'FEED_URI': 'output/business.xlsx'
})
process.crawl(BBBSpider)
process.start()
