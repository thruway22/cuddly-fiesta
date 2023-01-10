import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import arabic_reshaper
from bidi.algorithm import get_display
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

st.subheader('P/FFO Ratio')

st.pyplot(chart_pffo(ticker, file_path='data.csv'))

df = prepare_data(file_path='data.csv')

col1, col2 = st.columns(2)

with col1:
    st.subheader('FFO Per Share')
    st.pyplot(chart_metric(df, ticker, 'ffos'))

with col2:
    st.subheader('FFO Payout Ratio')
    text = "ذهب الطالب الى المدرسة. ذهب الطالب الى المدرسة. ذهب الطالب الى المدرسة. ذهب الطالب الى المدرسة"
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    st.write(bidi_text)
    st.pyplot(chart_metric(df, ticker, 'ffo_payout'))
