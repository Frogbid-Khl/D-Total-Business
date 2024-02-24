import scrapy
from scrapy.crawler import CrawlerProcess


class BBBSpider(scrapy.Spider):
    name = "bbb_spider"

    start_urls = ["https://www.bbb.org/us/wy/cheyenne/category/wood-rot-repair"]

    def parse(self, response):
        try:
            total_element = response.xpath('//*[@id="content"]/div/div[2]/div/h1/strong[1]')
            total = total_element.get().strip() if total_element else None
            if total:
                print(total)
            else:
                print("Total element not found")
        except Exception as e:
            print("Error:", e)


process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'LOG_ENABLED': True  # Disable logging
})

process.crawl(BBBSpider)
process.start()
