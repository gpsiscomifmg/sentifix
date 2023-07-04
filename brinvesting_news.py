#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
BrInvesting IFIX News
'''

import time
import random
import os
import json
import requests
from bs4 import BeautifulSoup

# News attributes
AUTHOR = 'author'
AUTHOR_LINK = 'author_link'
CATEGORY = 'category'
DATE = 'date'
TIME = 'time'
TITLE = 'title'
CONTENT = 'content'
COMMENTS = 'comments'

# URLs
URL_BASE = 'https://br.investing.com'
URL_IFIX = URL_BASE + '/indices/bm-fbovespa-real-estate-ifix-news/'

# Files
LINKS_FILE = 'links.txt'
NEWS_FILE = 'news.json'

def get_source(url):
    '''
    Get source code from URL
    '''
    agent = {'User-Agent':'Mozilla/5.0'}
    # Random delay
    time.sleep(random.randint(2, 5))
    return requests.get(url, headers=agent, timeout=10).text

def update_links_from_page(page_number, link_list):
    '''
    Get links from page of news
    '''
    html = get_source(URL_IFIX + str(page_number))
    soup = BeautifulSoup(html, 'html.parser')
    # Find list of news
    lista = soup.find('ul', {'data-test': 'news-list'})
    if lista is None:
        return
    # Carry out links
    for link in lista.find_all('a', href=True):
        # Ignore links to comments
        if '#comments' not in link['href'][-9:]:
            # Final link URL
            final_link = URL_BASE + link['href']
            # Check if link does not exist
            if final_link not in link_list:
                print('Found new link: ' + final_link)
                # Add link to list
                link_list.append(final_link)

def update_links():
    '''
    Update new links
    '''
    link_list = []
    # Check if link file exists
    if os.path.isfile(LINKS_FILE):
        # Load existing links
        with open(LINKS_FILE, 'r', encoding='utf-8') as file:
            link_list = file.read().split('\n')[:-1]
    print('Getting links...')
    # Start page
    page_number = 1
    while True:
        print('Scanning links on page: ' + str(page_number))
        # Get current number of links
        current = len(link_list)
        # Update links for current page
        update_links_from_page(page_number, link_list)
        # If no new links were found, stop
        if len(link_list) == current:
            break
        # Go to next page
        page_number += 1
    # Save links to file
    with open(LINKS_FILE, 'w', encoding='utf-8') as file:
        for link in link_list:
            file.write(link + '\n')
    return link_list

def get_new(link):
    '''
    Get new content from link
    '''
    html = get_source(link)
    soup = BeautifulSoup(html, 'html.parser')
    # New dictionary
    new = {}
    # Title and category
    new[TITLE] = soup.find('h1', class_='articleHeader').text
    info = soup.find_all('div', class_='contentSectionDetails')
    author_info = info[0].find_all('a')
    new[CATEGORY] = author_info[0].text
    if len(author_info) > 1:
        new[AUTHOR] = author_info[0].text
        new[AUTHOR_LINK] = author_info[0]['href']
        new[CATEGORY] = author_info[1].text
    # Date and time
    date_time = info[1].text.split()
    new[DATE] = date_time[1]
    new[TIME] = date_time[2]
    # Content and comments
    content = soup.find('div', class_='articlePage')
    par_list = content.find_all('p', recursive=False)
    new[CONTENT] = ''
    for paragrafo in par_list[:-1]:
        new[CONTENT] += '\n' + paragrafo.text
    comments = soup.find('div', class_='commentsWrapper')
    comment_list = comments.find_all('div', class_='comment', recursive=False)
    new[COMMENTS] = ''
    for comment in comment_list:
        new[COMMENTS] += '\n' + comment.find('span', class_='js-text').text
    return new

def update_news(link_list):
    '''
    Update news from link list
    '''
    news = {}
    # Open news file
    if os.path.isfile(NEWS_FILE):
        with open(NEWS_FILE, 'r', encoding='utf-8') as file:
            news = json.load(file)
    # For each link
    for link in link_list:
        link = link.strip()
        # Check news is already downloaded
        if link not in news:
            print('Getting new: ' + link)
            news[link] = get_new(link)
            # Save news to file
            with open(NEWS_FILE, 'w', encoding='utf-8') as file:
                json.dump(news, file, indent=2, ensure_ascii=False)
            time.sleep(5)

def main():
    '''
    Main function
    '''
    print('BrInvesting IFIX News')
    link_list = update_links()
    update_news(link_list)

if __name__ == '__main__':
    main()