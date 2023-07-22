#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
IFIX History
'''

import requests
import pandas as pd
from base64 import b64encode
from datetime import datetime
from files import (DATE, IFIX, IFIX_FILE, load_ifix, to_float)

FIRST_IFIX_YEAR = 2010
URL_BASE = 'https://sistemaswebb3-listados.b3.com.br/indexStatisticsProxy/IndexCall/GetPortfolioDay/'

def get_history(year):
    '''
    Get IFIX history for year
    '''
    # Get API data
    params = '{"index":"IFIX","language":"pt-br","year":"' + str(year) + '"}'
    params = b64encode(params.encode())
    url = URL_BASE + str(params.decode())
    input_list = requests.get(url, timeout=10).json()
    # Carry out data (lines of days and columns of months)
    input_list = input_list['results']
    history_list = []
    for day_dict in input_list:
        day = day_dict['day']
        for month in range(1, 13):
            value = day_dict['rateValue' + str(month)]
            if value is not None:
                ifix_dict = {
                    DATE: str(year) + '-' + str(month) + '-' + str(day),
                    IFIX: to_float(value)
                }
                history_list.append(ifix_dict)
    return history_list

def update():
    '''
    Update IFIX data
    '''
    # Get current IFIX data
    ifix_data = load_ifix()
    if ifix_data is None:
        start_year = FIRST_IFIX_YEAR
        ifix_data = pd.DataFrame()
    else:
        start_year = ifix_data.index.max().year
        ifix_data = ifix_data[ifix_data.index.year < start_year]
    current_year = datetime.now().year
    hist_list = []
    # Get history for each year
    for year in range(start_year, current_year+1):
        print('Getting IFIX history for year', year)
        hist_list += get_history(year)
    # Build new data frame
    new_data = pd.DataFrame(hist_list)
    new_data.set_index(DATE, inplace=True)
    new_data.index = pd.to_datetime(new_data.index)
    # Update current data
    ifix_data = ifix_data.append(new_data)
    ifix_data.sort_index(inplace=True)
    ifix_data = ifix_data.resample('D').mean()
    ifix_data.fillna(method='ffill', inplace=True)
    ifix_data.to_csv(IFIX_FILE)

if __name__ == '__main__':
    update()
