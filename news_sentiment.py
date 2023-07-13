#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
News sentiment
'''

# https://medium.com/data-hackers/an%C3%A1lise-de-sentimentos-em-portugu%C3%AAs-utilizando-pytorch-e-python-91a232165ec0
# Leia (vader) (usar direto e estudar como atualizar lexicons)
# Traduzir e usar vader nativo da NLTK
# Sentlex-pt

import nltk
import numpy as np
import pandas as pd
from leia import SentimentIntensityAnalyzer
from files import DATE, TITLE, CONTENT, COMMENTS, get_news

ANALYZER = SentimentIntensityAnalyzer()

def summarize_sentiment(text):
    '''summarize sentiment from text'''
    content_list = nltk.sent_tokenize(text)
    sent_list = [ANALYZER.polarity_scores(sentence) for sentence in content_list]
    sentiment = {
        'neg': np.mean([item['neg'] for item in sent_list]),
        'neu': np.mean([item['neu'] for item in sent_list]),
        'pos': np.mean([item['pos'] for item in sent_list]),
        'compound': np.mean([item['compound'] for item in sent_list])
        }
    return sentiment

def get_sentiment(new):
    '''get sentiments from new'''
    sent_dict = {DATE: new[DATE]}
    title_sentiment = ANALYZER.polarity_scores(new[TITLE])
    content_sentiment = summarize_sentiment(new[CONTENT])
    comments_sentiment = summarize_sentiment(new[COMMENTS])
    for sent, value in title_sentiment.items():
        sent_dict['title_' + sent] = value
    content_sentiment = ANALYZER.polarity_scores(new[CONTENT])
    for sent, value in content_sentiment.items():
        sent_dict['content_' + sent] = value
    comments_sentiment = ANALYZER.polarity_scores(new[COMMENTS])
    for sent, value in comments_sentiment.items():
        sent_dict['comments_' + sent] = value
    return sent_dict

def main():
    '''
    Main function
    '''
    news_dict = get_news()
    news_list = list(news_dict.values())
    sent_list = []
    for new in news_list:
        sent_dict = get_sentiment(new)
        sent_list.append(sent_dict)
    data = pd.DataFrame(sent_list)
    data[DATE]=pd.to_datetime(data[DATE].astype(str), format='%d.%m.%Y')
    data.set_index(DATE, inplace=True)
    data = data.resample('D').mean()
    data.interpolate(method='time', inplace=True)
    data.to_csv('sentiment.csv')

if __name__ == '__main__':
    main()
