#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : music_chatbot.py
# Create date : 2019-08-15 13:54
# Modified date : 2019-08-15 14:16
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

from search_es import SearchEs

class MusicChatbot:
    def __init__(self):
        self.es_searcher = SearchEs()
        return

    def _get_origin(self, res):
        return res['singer'] + '的' + '《%s》' % res['song']

    def search_next(self, lyric):
        '''搜索下一句歌词'''
        res_context = self.es_searcher.next_geci(lyric)
        ret = []
        for res in res_context:
            next_sentence = res['next']
            _from = self._get_origin(res)
            if next_sentence != 'end':
                ret.append([next_sentence, _from])

        if not ret:
            return '没找着下一句，可能是我比较笨'
        else:
            return "\n".join(["下一句："]+['  ---来自'.join(i) for i in ret])

    def search_last(self, lyric):
        '''搜索上一句歌词'''
        res_context = self.es_searcher.next_geci(lyric)
        ret = []
        for res in res_context:
            last_sentence = res['last']
            _from = self._get_origin(res)
            if last_sentence != 'start':
                ret.append([last_sentence, _from])

        if not ret:
            return '没找着上一句，可能是我比较笨'
        else:
            return "\n".join(["上一句："]+['  ---来自'.join(i) for i in ret])

if __name__ == '__main__':
    handler = MusicChatbot()
    #lyric = '我爱你中国'
    lyric = '好好的一份爱啊怎么会慢慢变坏'
    next_sentence = handler.search_next(lyric)
    last_sentence = handler.search_last(lyric)
    print(next_sentence)
    print(last_sentence)
