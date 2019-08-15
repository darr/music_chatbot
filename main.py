#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : main.py
# Create date : 2019-08-15 14:04
# Modified date : 2019-08-15 14:35
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################
from __future__ import division
from __future__ import print_function

from insert_es import init_ES
from music_chatbot import MusicChatbot

def build_database():
    init_ES()

def query(query_sentence):
    handler = MusicChatbot()
    print("请问这句歌词的上下句：\n%s" % query_sentence)
    next_sentence = handler.search_next(query_sentence)
    last_sentence = handler.search_last(query_sentence)
    print(next_sentence)
    print(last_sentence)

def test_chatbot():

    query_sentence = '好好的一份爱啊怎么会慢慢变坏'
    query(query_sentence)

    query_sentence = '匆匆上路'
    query(query_sentence)

    query_sentence = '想要说声爱你'
    query(query_sentence)

    query_sentence = '原谅我这一生不羁放纵爱自由'
    query(query_sentence)

    query_sentence = '狼烟起江山北望'
    query(query_sentence)

def run():
    build_database()
    test_chatbot()

run()
