# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import print_function

#from scrapy import signals
import json
import boto3
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#Update data to DynamoDB
class DoubanmovieupdatePipeline(object): 
     
    def process_item(self, item, spider):
        dynamodb = boto3.resource('dynamodb',region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
        table = dynamodb.Table('Movies')
        print('updating table: ' + table.name)
        movie=dict(item)
        name = movie['name'][0]
        movie_id = movie['movieid']
        year = movie['year']
        score = movie['score']
        classification = movie['classification']
        url = movie['url']
        actor = movie['actor']
        director = movie['director']
                        
        print ("Adding movie: ", name)
                        
        response = table.put_item(
                                Item = {
                                       'name': name,
                                       'movie_id': movie_id,
                                       'year': year,
                                       'score': score,
                                       'classification': classification,
                                       'url': url,
                                       'actor': actor,
                                       'director': director
                                       }     
        )
                                                  
        print("PutItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))         
  
        return item
    
