# -*- coding: utf-8 -*-

'''
File utils
'''

import os
import json

# News attributes
AUTHOR = 'author'
AUTHOR_LINK = 'author_link'
CATEGORY = 'category'
DATE = 'date'
TIME = 'time'
TITLE = 'title'
CONTENT = 'content'
COMMENTS = 'comments'

# Files
LINKS_FILE = 'links.txt'
NEWS_FILE = 'news.json'

def get_links():
    '''Get links from file'''
    link_list = []
    # Check if link file exists
    if os.path.isfile(LINKS_FILE):
        # Load existing links
        with open(LINKS_FILE, 'r', encoding='utf-8') as file:
            link_list = file.read().split('\n')[:-1]
    # Save links to file
    return link_list

def save_links(link_list):
    '''Save links to file'''
    with open(LINKS_FILE, 'w', encoding='utf-8') as file:
        for link in link_list:
            file.write(link + '\n')

def get_news():
    '''Get news from file'''
    news = {}
    # Open news file
    if os.path.isfile(NEWS_FILE):
        with open(NEWS_FILE, 'r', encoding='utf-8') as file:
            news = json.load(file)
    return news

def save_news(news):
    '''Save news to file'''
    with open(NEWS_FILE, 'w', encoding='utf-8') as file:
        json.dump(news, file, indent=2, ensure_ascii=False)