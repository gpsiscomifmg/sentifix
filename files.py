# -*- coding: utf-8 -*-

'''
File utils
'''

import os
import json
import pandas as pd

# News attributes
AUTHOR = 'author'
AUTHOR_LINK = 'author_link'
CATEGORY = 'category'
DATE = 'date'
TIME = 'time'
TITLE = 'title'
CONTENT = 'content'
COMMENTS = 'comments'
# IFIX attributes
IFIX = 'ifix'

# Files
LINKS_FILE = 'data/links.txt'
NEWS_FILE = 'data/news.json'
IFIX_FILE = 'data/ifix.csv'
SENTIMENT_FILE = 'data/sentiment.csv'
STOPS_FILE = 'data/stops.txt'

def _load_from(file_name):
    '''Load list from TXT file'''
    item_list = []
    # Check if link file exists
    if os.path.isfile(file_name):
        # Load file content
        with open(file_name, 'r', encoding='utf-8') as file:
            item_list = file.read().split('\n')[:-1]
    return item_list

def _save_to(item_list, file_name):
    '''
    Save list to TXT file
    '''
    with open(file_name, 'w', encoding='utf-8') as file:
        for item in item_list:
            file.write(item + '\n')

def _load_from_json(file_name):
    '''
    Load from JSON file
    '''
    content = None
    if os.path.isfile(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            content = json.load(file)
    return content

def _save_to_json(content, file_name):
    '''
    Save to JSON file
    '''
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=2, ensure_ascii=False)

def load_links():
    '''
    Load links from file
    '''
    return _load_from(LINKS_FILE)

def save_links(link_list):
    '''
    Save links to file
    '''
    _save_to(link_list, LINKS_FILE)

def load_stops():
    '''
    Load stop words from file
    '''
    return _load_from(STOPS_FILE)

def load_news():
    '''
    Load news from file
    '''
    return _load_from_json(NEWS_FILE)

def save_news(news):
    '''
    Save news to file
    '''
    _save_to_json(news, NEWS_FILE)

def _load_pandas_csv(file_name, index_col=None):
    '''
    Load CSV file using Pandas
    '''
    data = None
    if os.path.isfile(file_name):
        if index_col:
            data = pd.read_csv(file_name, index_col=index_col, parse_dates=True)
        else:
            data = pd.read_csv(file_name, parse_dates=True)
    return data

def load_ifix():
    '''
    Load IFIX history from file
    '''
    return _load_pandas_csv(IFIX_FILE, index_col=DATE)

def to_float(text):
    '''
    Convert text to float
    '''
    text = text.replace('.', '')
    text = text.replace(',', '.')
    return float(text)
