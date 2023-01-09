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


tickers = [4330, 4331, 4332, 4333, 4334, 4335, 4336, 4337, 4338, 4339,
           4340, 4342, 4344, 4345, 4346, 4347, 4348]

ticker = st.selectbox('Which ticker?', tickers)

st.pyplot(chart_pffo(ticker, file_path='data.csv'))


