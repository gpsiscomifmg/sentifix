#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
News word count
'''

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from wordcloud import WordCloud
# ntlk.download('stopwords')
# nltk.download('punkt')

from files import TITLE, CONTENT, COMMENTS, get_news

news = get_news()

text = ''

for new in news.values():
    text += new[TITLE] + '\n' + new[CONTENT] + '\n' + new[COMMENTS]

words = word_tokenize(text.lower())
stops = stopwords.words('portuguese')
stops.extend(list(punctuation))
stops.extend(['fundo', 'r', 'fundos', 'sa', 'ifix', 'fii'])
words = list(filter(lambda word: word not in stops, words))

cloud = WordCloud(stopwords=stops, max_words=300, width=1600, height=800).generate(' '.join(words)) 

plt.figure(figsize=(15, 10), facecolor='k')
plt.imshow(cloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

freq = nltk.FreqDist(words)
freq.plot(50)
