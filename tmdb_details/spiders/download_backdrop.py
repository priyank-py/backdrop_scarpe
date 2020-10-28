import scrapy
import csv
import random
import json
import re


class DownloadBackdropSpider(scrapy.Spider):
    name = 'download_backdrop'
    count = 0
    # start_urls = ['http://x.com/']

    def start_requests(self):
        with open('m_v1_moview_with_backdrop_all.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['backdrops']:
                    self.count += 1
                    images = json.loads(row['backdrops'])
                    names = json.loads(row['local_backdrop_links'])
                    for image, name in zip(images, names):
                        yield scrapy.Request(image, callback=self.parse, meta={'dict': row, 'name': name})
                    
    def parse(self, response):
        name = response.meta.get('name')
        with open(f'backdrops/{name}', 'wb') as f:
            print(self.count)
            f.write(response.body)
