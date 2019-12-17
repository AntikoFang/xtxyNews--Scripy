# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 22:20:14 2019

@author: AntikoFang
"""
import requests

def get_data(url):
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r.text
