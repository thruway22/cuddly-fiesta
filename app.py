import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime  
from datetime import timedelta
from pandas.tseries.offsets import DateOffset
from pandas.tseries.offsets import MonthEnd
import steamlit as st
from utilities import *

st.title('SaudiREITsInfo')




tickers = {    
    4330: '4330: Riyad REIT',
    4331: '4331: Aljazira REIT',
    4332: '4332: Jadwa REIT Alharamain',
    4333: '4333: Taleem REIT',
    4334: '4334: Almaather REIT',
    4335: '4335: Musharaka REIT',
    4336: '4336: Mulkia Gulf REIT',
    4337: '4337: SICO Saudi REIT',
    4338: '4338: Alahli REIT',
    4339: '4339: Derayah REIT',
    4340: '4340: Alrajhi REIT',
    4342: '4342: Jadwa REIT',
    4344: '4344: SEDCO Capital REIT',
    4345: '4345: Alinma Retail REIT',
    4346: '4346: MEFIC REIT',
    4347: '4347: Bonyan REIT',
    4348: '4348: Alkhabeer REIT'
}

ticker = st.selectbox('Choose a REIT fund', tickers.keys(),
                      format_func=lambda x:tickers[x])

st.subheader('Price')

st.pyplot(chart_timeseries_data(ticker, 'price'))

st.subheader('P/FFO')

st.pyplot(chart_timeseries_data(ticker, 'pffo'))

st.subheader('Yield')

st.pyplot(chart_timeseries_data(ticker, 'yield'))

col1, col2 = st.columns(2)

with col1:
    st.subheader('FFO Per Share')
    st.pyplot(chart_categorical_data(ticker, 'ffos'))
    
    st.subheader('FFO Payout Ratio')
    st.pyplot(chart_categorical_data(ticker, 'ffo_payout'))
    
    st.subheader('roic')
    st.pyplot(chart_categorical_data(ticker, 'roic'))
with col2:
    st.subheader('op_margin')
    st.pyplot(chart_categorical_data(ticker, 'op_margin'))
    
    st.subheader('net_debt_ebitda')
    st.pyplot(chart_categorical_data(ticker, 'net_debt_ebitda'))
    
    st.subheader('net_debt_capital')
    st.pyplot(chart_categorical_data(ticker, 'net_debt_capital'))
    
    st.subheader('coverage')
    st.pyplot(chart_categorical_data(ticker, 'coverage'))
    
