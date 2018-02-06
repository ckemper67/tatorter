# -*- coding: utf-8 -*-
'''
Created on 05.02.2018

@author: DLF
'''
from fuzzywuzzy import fuzz
import os

class Episode(object):
    def __init__(self, **kwargs):
        self._attribs = []
        for key, val in kwargs.items():
            setattr(self, key, val)
            self._attribs.append(key)
        for must_have in ["episode_index","title","location","broadcaster"]:
            assert must_have in self._attribs
    @property
    def as_dict(self):
        result = {}
        for attrib in self._attribs:
            result[attrib] = getattr(self, attrib)
        return result
    def match(self, file_name):
        file_name = os.path.splitext(os.path.basename(file_name))[0].lower()
        title = self.title.lower()
        broadcaster = self.broadcaster.lower()
        value = fuzz.partial_ratio(title, file_name)
        #max 100
        if broadcaster in file_name:
            value +=10
        #max 110
        if str(self.episode_index) in file_name:
            value += 5 * len(str(self.episode_index))
        #max 130
        value = int(100 * value / 130)
        return value  
        
    
class Matcher(object):
    def __init__(self, file_name, episodes):
        self.match_list = []
        for episode in episodes:
            value = episode.match(file_name)
            self.match_list.append((value, episode))
        self.match_list.sort(key=lambda e:e[0], reverse=True)
    