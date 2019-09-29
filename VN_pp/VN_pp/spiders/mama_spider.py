import scrapy


class MamaSpider(scrapy.Spider):
    name = 'mama_links'

    def start_requests(self):
        urls = [
            # "https://vnexpress.net/thoi-su",
            # "https://vnexpress.net/the-gioi",
            # "https://vnexpress.net/kinh-doanh",
            # "https://vnexpress.net/giai-tri",
            # 'https://vnexpress.net/the-thao',
            # "https://vnexpress.net/phap-luat",
            # "https://vnexpress.net/giao-duc",
            # "https://vnexpress.net/suc-khoe",
            # "https://vnexpress.net/doi-song",
            # "https://vnexpress.net/du-lich",
            # "https://vnexpress.net/khoa-hoc",
            # "https://vnexpress.net/so-hoa",
            'https://vnexpress.net/oto-xe-may',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        links = response.xpath('//article[@class="list_news"]/h4[@class="title_news"]/a[1]/@href').getall()

        with open('./data/oto-xe-may.txt', 'a') as f:
            for link in links:
                f.write(link + '\n')

        print('LINKS: {}'.format(links))

        next_page = response.xpath('//*[@id="pagination"]/a[@class="next"]/@href').get()
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
