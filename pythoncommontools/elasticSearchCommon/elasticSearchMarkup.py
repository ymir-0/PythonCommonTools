# coding=utf-8
# imports
from enum import Enum, unique
# record
@unique
class RecordFieldMarkup( Enum ):
    hits = "hits"
    id = "_id"
    index = "_index"
    found = "found"
    source = "_source"
