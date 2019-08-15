#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : insert_es.py
# Create date : 2019-08-15 13:38
# Modified date : 2019-08-15 14:48
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

import os
import time
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from etc import ES_IP
from etc import ES_PORT
from etc import DATA_PATH

class ProcessIntoES:
    def __init__(self):
        self._index = "music_data"
        self.es = Elasticsearch([{"host": ES_IP, "port": ES_PORT}])
        self.doc_type = "music"
        cur = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.music_file = os.path.join(cur, DATA_PATH)

    def create_mapping(self):
        '''创建ES索引，确定分词类型'''
        node_mappings = {
            "mappings": {
                self.doc_type: {    # type
                    "properties": {
                        "geci": {    # field: 歌词内容
                            "type": "text",    # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"    # The index option controls whether field values are indexed.
                        },
                        "song":{    # field: 歌曲名称
                            "type": "text",    # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"    # The index option controls whether field values are indexed.
                        },
                        "album": {  # field: 歌词所属专辑
                            "type": "text",  # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"  # The index option controls whether field values are indexed.
                        },
                        "singer": {  # field: 歌手
                            "type": "text",  # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"  # The index option controls whether field values are indexed.
                        },
                        "composer": {  # field: 歌手
                            "type": "text",  # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"  # The index option controls whether field values are indexed.
                        },
                        "author": {  # field: 歌手
                            "type": "text",  # lxw NOTE: cannot be string
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart",
                            "index": "true"  # The index option controls whether field values are indexed.
                        },
                    }
                }
            }
        }
        if not self.es.indices.exists(index=self._index):
            self.es.indices.create(index=self._index, body=node_mappings)
            print("Create {} mapping successfully.".format(self._index))
            return False
        else:
            print("index({}) already exists.".format(self._index))
            return True

    def insert_data_bulk(self, action_list):
        '''批量插入数据'''
        success, _ = bulk(self.es, action_list, index=self._index, raise_on_error=True)
        print("Performed {0} actions. _: {1}".format(success, _))

    def search_specific(self, value, key="name"):
        '''根据title进行事件的匹配查询'''
        query_body = {
            "query": {
                "match": {
                    key: value,
                }
            }
        }
        searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=100)
        # 输出查询到的结果
        return searched["hits"]["hits"]

def collect_events():
    '''根据建立的因果知识图谱，获取原因事件集合，结果事件集合'''
    titles = []
    for line in open('title.txt'):
        line = line.strip()
        if not line:
            continue
        titles.append(line)
    return titles

def init_ES():
    '''初始化ES，将数据插入到ES数据库当中'''
    pie = ProcessIntoES()
    # 创建ES的index
    ret = pie.create_mapping()
    if ret:
        return
    start_time = time.time()
    index = 0
    count = 0
    action_list = []
    BULK_COUNT = 2000  # 每BULK_COUNT个句子一起插入到ES中
    for line in open(pie.music_file):
        if not line:
            continue
        item = json.loads(line)
        index += 1
        action = {
            "_index": pie._index,
            "_type": pie.doc_type,
            "_source": {
                "song": item['song'],
                "singer": item['singer'],
                "album": item['album'],
                "geci": '\n'.join(item['geci']),
                "compser": item['composer'],
                "author": item['author']
            }
        }
        action_list.append(action)
        if index > BULK_COUNT:
            pie.insert_data_bulk(action_list=action_list)
            index = 0
            count += 1
            print(count)
            action_list = []
        end_time = time.time()
        print("Time Cost:{0}".format(end_time - start_time))

def news_search(title):
    '''根据标题，显示匹配结果'''
    if not title:
        return []
    pie = ProcessIntoES()
    searched_result = pie.search_specific(title)
    search_result = []
    for hit in searched_result:
        # print(hit)
        source_dict = hit
        print(source_dict)
    return search_result

if __name__ == "__main__":
    # handler = ProcessIntoES()
    # title = '螺纹钢大涨'
    # 将数据库插入到elasticsearch当中
    init_ES()
    # 按照标题进行查询
    # news_search(title)
    # handler.create_index()

