#! /bin/bash



export PATH=$PATH:/Users/luyingqi/anaconda/bin

cd /Users/luyingqi/Documents/bittiger/group_project_craw_recom/crawler/doubanMovieUpdate/doubanMovieUpdate

scrapy crawl movieUpdate > /tmp/test.log 2>&1 &

