#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
News sentiment using leia (VADER)
'''

import pandas as pd
from leia import SentimentIntensityAnalyzer
from files import DATE, TITLE, CONTENT, COMMENTS, SENTIMENT_FILE, get_news

ANALYZER = SentimentIntensityAnalyzer()

def get_sentiment(new):
    '''
    get sentiments from new
    '''
    sent_dict = {DATE: new[DATE]}
    title_sentiment = ANALYZER.polarity_scores(new[TITLE])
    content_sentiment = ANALYZER.polarity_scores(new[CONTENT])
    comments_sentiment = ANALYZER.polarity_scores(new[COMMENTS])
    for sent, value in title_sentiment.items():
        sent_dict['title_' + sent] = value
    content_sentiment = ANALYZER.polarity_scores(new[CONTENT])
    for sent, value in content_sentiment.items():
        sent_dict['content_' + sent] = value
    comments_sentiment = ANALYZER.polarity_scores(new[COMMENTS])
    for sent, value in comments_sentiment.items():
        sent_dict['comments_' + sent] = value
    return sent_dict

def update():
    '''
    Main update function
    '''
    news_dict = get_news()
    sent_list = []
    # Compute sentiment for each new
    for new in news_dict.values():
        sent_dict = get_sentiment(new)
        sent_list.append(sent_dict)
    # Build data frame
    data = pd.DataFrame(sent_list)
    data[DATE]=pd.to_datetime(data[DATE].astype(str), format='%d.%m.%Y')
    data.set_index(DATE, inplace=True)
    # Resample and interpolate
    data = data.resample('D').mean()
    data.interpolate(method='time', inplace=True)
    data.to_csv(SENTIMENT_FILE)

if __name__ == '__main__':
    update()
