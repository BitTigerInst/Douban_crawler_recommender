import scrapy
import json
import re
from scrapy.selector import Selector
from doubanMovieUpdate.items import DoubanmovieupdateItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class DoubanUpdate(CrawlSpider):
    name = "movieUpdate"
    allowed_domains = ["douban.com"]
    items_id = set()
    start_urls = [
        "https://movie.douban.com/nowplaying/beijing/"
    ]
 
    rules=(
        #Rule(LinkExtractor(allow=(r'https://movie.douban.com/nowplaying/beijing/',))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/\?from=playing_poster',)),callback="parse_item"),
    )

    
    def parse_item(self, response):
        sel=Selector(response)
        item=DoubanmovieupdateItem()
        item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//strong[@class="ll rating_num"]/text()').extract()
        item['cover'] = sel.xpath('//div[@id="mainpic"]/a/@href').extract_first()
        item_preurl = response.url
        movieid = re.match(r'https://.*/.*/(.*)/.*', item_preurl).group(1)
        item['url']=r'http://movie.douban.com/subject/'+movieid+r'/'
        item['movieid'] =movieid
        item['director']=sel.xpath('//span[@class="attrs"]/a[@rel="v:directedBy"]/text()').extract()
        item['classification']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        #item['actor']= sel.xpath('//*[@id="info"]/span[3]/a[1]/text()').extract()
        item['actor']= sel.xpath('//span[@class="attrs"]/a[@rel="v:starring"]/text()').extract()
        
        yield item

