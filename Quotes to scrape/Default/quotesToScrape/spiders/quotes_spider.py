from pathlib import Path
import scrapy
from scrapy.selector import Selector

class QuotesScrapy(scrapy.Spider):
    name = 'quotes'

    start_urls = [
        "https://quotes.toscrape.com/"
    ]

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')

        for quote in quotes:
            yield {
                "quote": quote.xpath('span[@class="text"]/text()').get().strip("“”"),
                "author": quote.xpath('span[2]/small/text()').get(),
                "author_link": "https://quotes.toscrape.com" + quote.xpath('span[2]/a').attrib['href'],
                "tags": quote.xpath('div/a/text()').getall()
            }

        next_page = response.xpath('//li[@class="next"]/a').attrib["href"]
        if next_page is not None:
            next_page_url = "https://quotes.toscrape.com" + next_page
            yield response.follow(next_page_url, callback=self.parse)
