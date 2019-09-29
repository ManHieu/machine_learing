import scrapy
import re
import random


class QuotesSpider(scrapy.Spider):
    name = 'single_paper'

    def start_requests(self):
        urls = [
            # 'https://vnexpress.net/kinh-doanh/sep-thanh-tra-bo-cong-thuong-ve-tong-cuc-quan-ly-thi-truong-3989039.html?vn_source=Folder&vn_campaign=Stream&vn_medium=Item-5&vn_term=Desktop&vn_thumb=1',
        ]
        with open("./data/thoi-su.txt") as f:
            urls.extend(f.read().split('\n')) 

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        body = response.xpath('string(//article)').get()
        title = response.xpath('//title/text()').getall()
        key_word = response.xpath('//head/meta[@name="keywords"]/@content').get()
        topic = response.xpath('//head/meta[@name="its_subsection"]/@content').get()
        news_id = response.xpath('//head/meta[@name="tt_article_id"]/@content').get()
        
        content = re.sub('\n+', '\n', body)
        # topic = topic.split(",")

        with open("./data/thoi-su/{}.txt".format(news_id), 'w') as f:
            f.write("TITLE: " + title[0] + '\n\n')
            f.write("KEY WORDS: " + key_word + "\n\n")
            f.write("TOPIC: " + topic + "\n\n")
            f.write("CONTENT: " + content)

        print("TITLE: {}".format(title[0]))
        print("CONTENT: {}".format(content))
        print("KEYWORDS: {}".format(key_word))
        print("TOPIC: {}".format(topic))
        print("NEWS_ID: {}".format(news_id))