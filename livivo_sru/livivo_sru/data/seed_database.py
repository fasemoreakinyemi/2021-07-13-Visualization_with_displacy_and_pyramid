#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from pymongo import MongoClient
import json
from bson.json_util import loads
import pymongo

#articles = []
#for line in open("/home/mandela/Doctoral/2021-07-08_document_visualization_with_spacy/livivo_sru/livivo_sru/data/json/coxiella_burnetii.json",
#                 "r",
#                 encoding="utf8"):
#    articles.append(loads(line.strip()))
client = MongoClient('localhost', 27017)
db = client['coxiella_articles']
collection = db['articles_collection']
#collection.insert_many(articles)
collection.drop_indexes()
collection.create_index([
    ('liv.orig_data.ABSTRACT', pymongo.TEXT),
    ('liv.orig_data.TITLE', pymongo.TEXT)
], name="titel_and_abstract_index")

print(collection.index_information())





