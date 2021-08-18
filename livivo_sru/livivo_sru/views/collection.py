from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId    
import json
    
@view_config(route_name='collections',
             renderer='livivo_sru:templates/collections.jinja2')
def collections(request):
    client = MongoClient('localhost', 27017)
    db = client['articles_collection']
    collection = db['collection_names']
    query = collection.find()
    return {"results": query}

@view_config(route_name='collections_post_api', renderer='json')
def collection_post_api(request):
    client = MongoClient('localhost', 27017)
    db = client['articles_collection']
    collection = db['collection_names']
    input_dict = {"name": request.params['name'],
                  "owner": request.params['owner']}
    query = collection.find({"name": request.params['name']})
    if query.count() > 0:
        return{"results": "exists"}
    else:
        collection.insert_one(input_dict)
        return {"results": "success"}

@view_config(route_name='insert_collection_api', renderer='json')
def insert_collection_api(request):
    client = MongoClient('localhost', 27017)
    db = client['articles_collection']
    collection = db['collection_table']
    input_dict = {"collection_name": request.params['name'],
                  "article_id": request.params['id']}
    query = collection.find({"article_id": request.params['id']})
    if query.count() > 0:
        return{"results": "exists"}
    else:
        collection.insert_one(input_dict)
        return {"results": "success"}

@view_config(route_name='collection_view',
             renderer='livivo_sru:templates/collection_view.jinja2')
def collection_view(request):
    client = MongoClient('localhost', 27017)
    db = client['articles_collection']
    collection = db['collection_table']
    collection_name = request.matchdict["collection"]
    print(collection_name)
    query = collection.find({"collection_name": collection_name})
    print(query.count())
    id_list = [ObjectId(aid["article_id"]) for aid in query]
    db = client['coxiella_articles']
    collection = db['articles_collection']
    query = collection.find({"_id":{ "$in" : id_list}})
    print(query.count())
    return {"results": query}

