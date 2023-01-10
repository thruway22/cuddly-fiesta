import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utilities import *

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
    '4330: Riyad REIT': 4330,
    '4331: Aljazira REIT': 4331,
    '4332: Jadwa REIT Alharamain': 4332,
    '4333: Taleem REIT': 4333,
    '4334: Almaather REIT': 4334,
    '4335: Musharaka REIT': 4335,
    '4336: Mulkia Gulf REIT': 4336,
    '4337: SICO Saudi REIT': 4337,
    '4338: Alahli REIT': 4338,
    '4339: Derayah REIT': 4339,
    '4340: Alrajhi REIT': 4340,
    '4342: Jadwa REIT': 4342,
    '4344: SEDCO Capital REIT': 4344,
    '4345: Alinma Retail REIT': 4345,
    '4346: MEFIC REIT': 4346,
    '4347: Bonyan REIT': 4347,
    '4348: Alkhabeer REIT' 4348}

ticker = st.selectbox('Which ticker?', tickers.values())

st.subheader('P/FFO Ratio')

st.pyplot(chart_pffo(ticker, file_path='data.csv'))

df = prepare_data(file_path='data.csv')

col1, col2 = st.columns(2)

with col1:
    st.subheader('FFO Per Share')
    st.pyplot(chart_metric(df, ticker, 'ffos'))

with col2:
    st.subheader('FFO Payout Ratio')
    st.pyplot(chart_metric(df, ticker, 'ffo_payout'))
