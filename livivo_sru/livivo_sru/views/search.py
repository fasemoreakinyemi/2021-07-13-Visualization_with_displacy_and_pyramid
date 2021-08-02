from pyramid.view import view_config
from pyramid.response import Response
import json
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId    

@view_config(route_name='search', renderer='livivo_sru:templates/search.jinja2')
def search(request):
    return {}

@view_config(route_name='search_api', renderer='json')
def search_api(request):
    client = MongoClient('localhost', 27017)
    db = client['coxiella_articles']
    collection = db['articles_collection']
    
    if "search" in request.params:
        search = request.params['search']
    #query = collection.find().limit(10)
        query = collection.find(
            { "$text": {
                "$search": search }
            }).limit(10)

    if "articleId" in request.params:
        obj_id = request.params["articleId"]
        query = collection.find_one({'_id': ObjectId(obj_id)})
    
    
    results = dumps(query)

    return {"results": results}
#    query = collection.find({"$or": [
#        { "$text": {
#            "$search": search }
#        },
#        {
#            'liv["orig_data"]["ABSTRACT"]': {
#                "$regex": search,
#                "$options": 'i'
#            }
#        }
#                                    ]
#                                }
#                            ).limit(10)
#
#        {
#            'liv["orig_data"]["TITLE"]': {
#                "$regex": search,
#                "$options": 'i'
#            }
#        }
