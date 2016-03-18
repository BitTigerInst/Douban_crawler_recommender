from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def retrieve_movie_info():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('Movies')
    response = table.scan()
    movie_info = {}
    
    for movie in response[u'Items']:
        movie_id = movie['movie_id']
        name = movie['name']
        movie_info[movie_id] = {'name':name}

    return movie_info

def retrieve_user_review_history():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('Users')
    response = table.scan()
    user_review_history = {}

    for user in response[u'Items']:
        user_review_history[user['user_id']] = user['review_history']

    return user_review_history

def update_moive_recommend(movie, top_5_movie):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('Movie_Recommend')

    table.put_item(
         'movie_id': movie,
         'recommend':top_5_movie
    )

def update_user_movie_recommend(user_id, top_5_movie):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('Movie_User_Recommend')
    
    table.put_item(
        'user_id': user_id,
        'recommend':top_5_movie
    )

def update_user_recommend(user_id, top_5_user):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('User_Recommend')
    
    table.put_item(
        'user_id': user_id,
        'recommend':top_5_user
    )
