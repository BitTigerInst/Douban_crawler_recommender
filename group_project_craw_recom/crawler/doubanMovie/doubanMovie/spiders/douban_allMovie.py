import scrapy 
import json
import re
from scrapy.selector import Selector
from doubanMovie.items import DoubanmovieItem
from scrapy.spiders import CrawlSpider,Rule
#from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor

class DoubanAllMovie(CrawlSpider):
   name = "doubanAllMovie"
   allowed_domains = ["douban.com"]
   items_id = set()
   start_urls = [
    "https://douban.com/tag/%E7%BE%8E%E5%9B%BD/movie",
    "https://douban.com/tag/%E6%97%A5%E6%9C%AC/movie",
    "https://douban.com/tag/%E6%B8%AF%E5%8F%B0/movie",
    "https://douban.com/tag/%E8%8B%B1%E5%9B%BD/movie",
    "https://douban.com/tag/%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86/movie",
    "https://douban.com/tag/%E5%86%85%E5%9C%B0/movie",
    "https://douban.com/tag/%E9%9F%A9%E5%9B%BD/movie",
    "https://douban.com/tag/%E6%AC%A7%E6%B4%B2/movie",
    "https://douban.com/tag/%E4%BF%84%E7%BD%97%E6%96%AF/movie",
    "https://douban.com/tag/%E5%8D%97%E7%BE%8E/movie"
    # "http://movie.douban.com/top250"
    # "http://movie.douban.com/subject/19944106/"
   ]
   
   rules=(
        #Rule(LinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*',))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=15'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=30'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=45'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=60'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=75'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=90'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=105'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=120'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=135'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=150'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=165'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=180'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=195'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=210'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=225'))),
        Rule(LinkExtractor(allow=(r'https://www.douban.com/tag/.*/movie\?start=240'))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/.*',)),callback="parse_item"),
   )
   
   

   def parse_item(self, response):
        sel=Selector(response)
        print response.url
        item=DoubanmovieItem()
        item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//strong[@class="ll rating_num"]/text()').extract()
        item['cover'] = sel.xpath('//div[@id="mainpic"]/a/@href').extract_first()
        item_preurl = response.url
        movieid = re.match('https://.*/.*/(.*)/.*', item_preurl).group(1)
        #movieid = re.match(r'http://.*/.*/(.*)/.*', item_preurl).group(1)
        item['url']=r'https://movie.douban.com/subject/'+movieid+r'/'
        item['movieid'] =movieid
        #item['director']=sel.xpath('//*[@id="info"]/span[1]/a/text()').extract()
        item['director']=sel.xpath('//span[@class="attrs"]/a[@rel="v:directedBy"]/text()').extract()
        item['classification']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        #item['actor']= sel.xpath('//*[@id="info"]/span[3]/a[1]/text()').extract()
        item['actor']= sel.xpath('//span[@class="attrs"]/a[@rel="v:starring"]/text()').extract()
        
        yield item
       
  
