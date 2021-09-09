from pyramid.view import view_config
from pyramid.response import Response
import json
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId    
import os

@view_config(route_name='search', renderer='livivo_sru:templates/search.jinja2')
def search(request):
    return {}

@view_config(route_name='search_api', renderer='json')
def search_api(request):
    url = os.environ['ME_CONFIG_MONGODB_URL']
    client = MongoClient(url)
    db = client['coxiella_articles']
    collection = db['articles_collection']
    
    if "search" in request.params:
        search = request.params['search']
        phrase = '\"{}\"'.format(search)
    #query = collection.find().limit(10)
        query = collection.find(
            { "$text": {
                "$search": phrase }},
            {'score': {
                '$meta': 'textScore'}
            }).limit(10)

    if "articleId" in request.params:
        obj_id = request.params["articleId"]
        query = collection.find_one({'_id': ObjectId(obj_id)})
    
    
    results = dumps(query)

    return {"results": results}
