import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime  
from datetime import timedelta
from pandas.tseries.offsets import DateOffset
from pandas.tseries.offsets import MonthEnd
import streamlit as st
import streamlit.components.v1 as components
from utilities import *
from texts import *

# st.set_page_config(layout="wide")

style_fullscreen_button_css = """
    button[title="View fullscreen"] {
        background-color: #004170cc;
        right: 0;
        color: white;
        visibility: hidden;
    }

    button[title="View fullscreen"]:hover {
        background-color:  #004170;
        color: white;
        visibility: hidden;
        }
    """
st.markdown(
    "<style>"
    + style_fullscreen_button_css
    + "</styles>",
    unsafe_allow_html=True,
)

st.title('SaudiREITsInfo')

tickers = {    
    9999: 'Choose a fund',
    4330: '4330: Riyad REIT الرياض ريت',
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

ticker = st.selectbox('Choose fund', tickers.keys(), label_visibility='collapsed',
                      format_func=lambda x:tickers[x])

placeholder = st.empty()

if ticker == 9999:
    pass
else:
    with placeholder.container():
        
        #st.markdown(display_text('empty', texts_dict), unsafe_allow_html=True)
        st.pyplot(chart_timeseries_data(ticker, 'price'))
        
        timeseries_metrics_list = ['pffo', 'yield']
        
        for i in timeseries_metrics_list:
            st.markdown('<hr />', unsafe_allow_html=True)
            st.markdown(display_text(i, texts_dict), unsafe_allow_html=True)
            st.pyplot(chart_timeseries_data(ticker, i))
            
        #st.markdown('<hr />', unsafe_allow_html=True)

        col1a, col2a = st.columns(2)

        with col1a:
            metric = 'ffos'
            st.markdown('<hr />', unsafe_allow_html=True)
            st.markdown(display_text(metric, texts_dict), unsafe_allow_html=True)
            st.pyplot(chart_categorical_data(ticker, metric))
                
        with col2a:
            metric = 'ffo_payout'
            st.markdown('<hr />', unsafe_allow_html=True)
            st.markdown(display_text(metric, texts_dict), unsafe_allow_html=True)
            st.pyplot(chart_categorical_data(ticker, metric))
            
        col1b, col2b = st.columns(2)
       
        with col1b:
            metric = 'net_debt_ebitda'
            st.markdown('<hr />', unsafe_allow_html=True)
            #st.markdown(display_text(metric, texts_dict), unsafe_allow_html=True)
            st.pyplot(chart_categorical_data(ticker, metric))
                
        with col2b:
            metric = 'coverage'
            st.markdown('<hr />', unsafe_allow_html=True)
            #st.markdown(display_text(metric, texts_dict), unsafe_allow_html=True)
            st.pyplot(chart_categorical_data(ticker, metric))
            
