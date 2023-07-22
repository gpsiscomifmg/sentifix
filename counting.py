#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
News and words counting
'''

import nltk
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from files import DATE, TITLE, CONTENT, COMMENTS, get_news, get_stops

def word_cloud(words, stops):
    '''
    Generate word cloud
    '''
    # Create cloud
    cloud = WordCloud(stopwords=stops, max_words=300,
                      width=1600, height=800).generate(' '.join(words)) 
    # Plot cloud
    plt.figure(figsize=(15, 10), facecolor='k')
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

def freq_graph(words):
    '''
    Generate frequency graph
    '''
    freq = nltk.FreqDist(words)
    freq.plot(50)

def news_count(news):
    '''Count news by month'''
    month_count = {}
    # Count news
    for new in news.values():
        # Month format: YYYY-MM
        month = new[DATE].split('.')[2] + '-' + new[DATE].split('.')[1]
        if month not in month_count:
            month_count[month] = 0
        month_count[month] += 1
    # Sort by mount
    month_count = sorted(month_count.items(), key=lambda x: x[0])
    # Print results
    data = pd.DataFrame(month_count, columns=['Mês', 'Notícias'])
    data.plot(x='Mês', y='Notícias', kind='bar', figsize=(15, 10))
    plt.show()

def main():
    '''
    Main function
    '''
    news = get_news()
    text = ''
    for new in news.values():
        text += new[TITLE] + '\n' + new[CONTENT] + '\n' + new[COMMENTS]
    # Tokenize words
    words = word_tokenize(text.lower())
    # Remove stop words and punctuation
    stops = get_stops()
    words = [word for word in words
             if word not in stops]
    word_cloud(words, stops)
    freq_graph(words)
    news_count(news)

if __name__ == '__main__':
    main()
