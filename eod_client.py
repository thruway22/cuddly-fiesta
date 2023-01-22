import os
import pandas as pd 
from eod import EodHistoricalData
from app import tickers_dict

api_key = os.environ["API_KEY"]
client = EodHistoricalData(api_key)
resp = client.get_prices_eod('4330.SR', period='d', order='a', from_='2018-01-01')
df = pd.DataFrame(resp)[['date']]

for i in tickers_dict.keys():
    resp = client.get_prices_eod(str(i)+'.SR', period='d', order='a', from_='2018-01-01')
    df = df.merge(pd.DataFrame(resp)[['date', 'adjusted_close']].rename(columns={"adjusted_close": i}), on='date', how='left')
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    
df.to_csv('data/pdata.csv', index=False)
