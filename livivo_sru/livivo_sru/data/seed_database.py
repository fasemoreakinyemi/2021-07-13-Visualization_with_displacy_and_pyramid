#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from pymongo import MongoClient
import json
from bson.json_util import loads
import pymongo
import os

articles = []
for line in open("{}/livivo_sru/data/json/coxiella_burnetii.json".format(os.getcwd()),
                 "r", encoding="utf8"):
    articles.append(loads(line.strip()))
url = os.environ['ME_CONFIG_MONGODB_URL']
print(url)
client = MongoClient("mongodb://root:example@mongodb:27017")
db = client['coxiella_articles']
collection = db['articles_collection']
collection.insert_many(articles)
collection.create_index([
    ('liv.orig_data.ABSTRACT', pymongo.TEXT),
    ('liv.orig_data.TITLE', pymongo.TEXT)
], name="titel_and_abstract_index")

print(collection.index_information())





