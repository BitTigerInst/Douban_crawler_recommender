import re
from logging import getLogger

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

from doubanMovie.items import DoubanmovieItem


log = getLogger(__name__)


class DoubanAllMovie(CrawlSpider):
    name = "doubanAllMovie"
    allowed_domains = ["douban.com"]

    start_tags = {
        '%E7%BE%8E%E5%9B%BD',
        '%E6%97%A5%E6%9C%AC',
        '%E6%B8%AF%E5%8F%B0',
        '%E8%8B%B1%E5%9B%BD',
        '%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86',
        '%E5%86%85%E5%9C%B0',
        '%E9%9F%A9%E5%9B%BD',
        '%E6%AC%A7%E6%B4%B2',
        '%E4%BF%84%E7%BD%97%E6%96%AF',
        '%E5%8D%97%E7%BE%8E'
    }
    start_urls = ['https://douban.com/tag/{}/movie'.format(tag) for tag in start_tags]
    # "http://movie.douban.com/top250"
    items_id = set()

    page_rules = [Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start={}'.format(num)))) for num in
                  range(15, 255, 15)]
    rules = page_rules + [
        # Rule(LinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*',))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/.*')),callback="parse_item")
    ]

    def parse_item(self, response):
        selector = Selector(response)
        log.info('parsing: {}'.format(response.url))
        item = DoubanmovieItem()
        item['name'] = selector.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year'] = selector.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score'] = selector.xpath('//strong[@class="ll rating_num"]/text()').extract()

        movieid = re.match('https://.*/.*/(.*)/.*', response.url).group(1)
        item['movieid'] = movieid
        item['director'] = selector.xpath('//span[@class="attrs"]/a[@rel="v:directedBy"]/text()').extract()
        item['classification'] = selector.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor'] = selector.xpath('//span[@class="attrs"]/a[@rel="v:starring"]/text()').extract()

        # get the first recommended poster
        list_poster_url = 'https://movie.douban.com/subject/{}/photos?type=R'.format(movieid)
        yield scrapy.Request(list_poster_url, callback=self.parse_poster_url, meta={'item': item})

    def parse_poster_url(self, response):
        item = response.meta['item']
        selector = Selector(response)

        first_poster_thumb_url = selector.xpath('//*[@id="content"]/div/div[1]/ul/li[1]/div[1]/a/img/@src').extract_first()
        item['poster_url'] = first_poster_thumb_url.replace('thumb', 'photo')
        yield item
