#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
News word count
'''

import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from wordcloud import WordCloud
from files import TITLE, CONTENT, COMMENTS, get_news

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

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
    # Remove stopwords and punctuation
    stops = stopwords.words('portuguese')
    stops.extend(list(punctuation))
    words = list(filter(lambda word: word not in stops, words))
    word_cloud(words, stops)
    freq_graph(words)

if __name__ == '__main__':
    main()
