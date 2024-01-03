import scrapy
import re

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parseBook(self, response):
        info = response.xpath('//div[@class="col-sm-6 product_main"]')
        textToNum = { "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5 }
        title = info.xpath('h1/text()').get().replace('"', '&quot;')
        
        yield {
            "title":        info.xpath('h1/text()').get(),
            "price":        float(info.xpath('p[@class="price_color"]/text()').get().replace("£", "")),
            "stock":        int(re.findall(r"\d+", info.xpath('p[@class="instock availability"]/text()')[-1].get())[0]),
            "stars":        textToNum[info.xpath('p[starts-with(@class, "star-rating")]').attrib["class"].split()[-1]],
            "book_url":     response.url,
            "image_url":    "https://books.toscrape.com" + response.xpath('//img')[0].attrib["src"][5:],
            "category":     response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').get(),
            "number":       int(re.findall(r'\d+', response.url)[-1])
        }

    def parse(self, response):
        books = response.xpath('//article[@class="product_pod"]')

        links = []
        for book in books:
            link = book.xpath('h3/a').attrib["href"]
            if "catalogue" in link:
                link_url = "https://books.toscrape.com/" + link
            else:
                link_url = "https://books.toscrape.com/catalogue/" + link

            yield response.follow(link_url, callback=self.parseBook)

        next_page = response.xpath('//li[@class="next"]/a')
        if next_page != []:
            next_page = next_page.attrib["href"]
            if "catalogue" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page

            yield response.follow(next_page_url, callback=self.parse)