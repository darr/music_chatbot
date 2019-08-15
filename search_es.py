#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : search_es.py
# Create date : 2019-08-15 13:42
# Modified date : 2019-08-15 14:37
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

from elasticsearch import Elasticsearch
import re

from etc import ES_IP
from etc import ES_PORT

class SearchEs:
    def __init__(self):
        self._index = "music_data"
        self.es = Elasticsearch([{"host": ES_IP, "port": ES_PORT}])
        self.doc_type = "music"

    def search_singer(self, singer):
        '''查询歌手，singer'''
        query_body = {
            "query": {
                "match": {
                    "singer": singer,
                }
            }
        }
        #searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=20)
        searched = self.es.search(index=self._index, body=query_body, size=20)
        # 输出查询到的结果
        return searched["hits"]["hits"]

    def search_geci(self, geci):
        '''查询歌词，geci'''
        query_body = {
            "query": {
                "match": {
                    "geci": geci,
                }
            }
        }
        #searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=20)
        searched = self.es.search(index=self._index, body=query_body, size=20)
        # 输出查询到的结果
        return searched["hits"]["hits"]

    def search_composer(self, composer):
        '''查询作曲者'''
        query_body = {
            "query": {
                "match": {
                    "compser": composer,
                }
            }
        }
        #searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=20)
        searched = self.es.search(index=self._index, body=query_body, size=20)
        # 输出查询到的结果
        return searched["hits"]["hits"]

    def search_author(self, author):
        '''查询作词者'''
        query_body = {
            "query": {
                "match": {
                    "composer": author,
                }
            }
        }
        #searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=20)
        searched = self.es.search(index=self._index, body=query_body, size=20)
        # 输出查询到的结果
        return searched["hits"]["hits"]

    def has_english(self, str):
        '''判断一个字符串是否包含英文'''
        for ch in str:
            if ch.lower() in ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
                return True

    def next_geci(self, geci):
        '''根据当前歌词，获取下一句歌词'''
        res_gecis = self.search_geci(geci)
        context = []
        for res in res_gecis:
            geci_list = []
            _gecis = res['_source']['geci'].split('\n')
            for _tmp in _gecis:
                if not self.has_english(_tmp):
                    _tmps = [i for i in re.split(r'[ \t\r\n]',_tmp) if i]
                else:
                    _tmps = [_tmp]
                geci_list += _tmps
            song = res['_source']['song']
            singer = res['_source']['singer']
            album = res['_source']['album']
            if geci in geci_list:
                last = 'start'
                next = 'end'
                data = {}
                data['song'] = song
                data['singer'] = singer
                data['album'] = album
                cur_index = geci_list.index(geci)
                if cur_index == 0:
                    last = 'start'
                    next = geci_list[cur_index - 1]
                elif cur_index == len(geci_list)-1:
                    last = geci_list[cur_index - 1]
                    next = 'end'
                else:
                    last = geci_list[cur_index-1]
                    next = geci_list[cur_index+1]

                if last != 'start' or next != 'end':
                    data['cur'] = geci
                    data['last'] = last
                    data['next'] = next
                    context.append(data)
        return context

    def search_song(self, song):
        '''查询歌曲，song'''
        query_body = {
            "query": {
                "match_phrase": {
                    "song": song,
                }
            }
        }
        #searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=1)
        searched = self.es.search(index=self._index, body=query_body, size=2)
        # 输出查询到的结果
        return searched["hits"]["hits"]

if  __name__ == '__main__':
    handler = SearchEs()
    #song = '能不能给我一首歌的时间'
    song = '冰雨'
    print("歌 《%s》：" % song)
    res_song = handler.search_song(song)
    print(res_song)
    singer = '许嵩'
    res_singer = handler.search_singer(singer)
    #print(res_singer)
    geci = '我是在等待一个女孩'
    print("%s 的下一句：" % geci)
    res_context = handler.next_geci(geci)
    print(res_context)
    geci = '好好的一份爱啊怎么会慢慢变坏'
    print("%s 的下一句：" % geci)
    res_context = handler.next_geci(geci)
    print(res_context)
