import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df_ffos = pd.read_csv('data.csv')

def compute_pffo(df):
    df['PFFO'] = (df.Close * df.Shares) / df.FFO
    df = df[['PFFO']]
    return df

def get_sector_pffo(df, ticker_col, year_col):
    
    # get only last ffo from input df and set index to ticker
    df = df[df[year_col] == df[year_col].max()].set_index(ticker_col)
    
    # get prices
    price_list = []
    
    for i in df.index:
        price = round(yf.Ticker(str(i)+'.SR').history(period='1d', interval='1d')['Close'][0], 2)
        price_list.append(price)
    
    # add to df
    df['Close'] = price_list
    
    # compute pff
    df = compute_pffo(df)
    
    return round(df.mean()[0], 2) #, round(df.median()[0], 2)
  
def get_pffo(ticker, df_ffos):
    
    # Concat to produce correct ticker format
    ticker_adj = str(ticker)+".SR"
    
    # get aux dataframe
    df_ffos = df_ffos[df_ffos['Ticker']==ticker][['Fiscal Year', 'Shares', 'FFO']]
    df_ffos['Fiscal Year'] = pd.to_datetime(df_ffos['Fiscal Year'], format='%Y')
    
    # get prices
    df_prices = yf.Ticker(ticker_adj).history(period='5y', interval='1d', actions=False)
    
    # select only close col and rest index
    df_prices = df_prices[['Close']].reset_index()
    
    # merge
    df_output = pd.merge(df_prices, df_ffos,
                         left_on = df_prices['Date'].apply(lambda x: (x.year)),
                         right_on = df_ffos['Fiscal Year'].apply(lambda y: (y.year)),
                         how = 'left')
    
    # change date (needed?)
    df_output['Date'] = df_output['Date'].dt.date
    
    # take only needed columns, set index, fillna
    df_output = df_output[['Date', 'Close', 'Shares', 'FFO']].set_index('Date').fillna(method='ffill')
    
    # add PFFO column
    #df_output['PFFO'] = (df_output.Close * df_output.Shares) / df_output.FFO
    
    # Get only needed data
    #df_output = df_output[['PFFO']]
    
    df_output = compute_pffo(df_output)
    
    ########
    
    # get current pffo
    current_pffo = round(df_output.tail(1)['PFFO'][0], 2)
    
    # get mean pffo
    mean_pffo = round(df_output.mean()[0], 2)
    
    return df_output, current_pffo, mean_pffo

sector_pffo = get_sector_pffo(df_ffos, 'Ticker', 'Fiscal Year')

  
##########
##########
##########

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

test_df, current_pffo, mean_pffo = get_pffo(ticker, df_ffos)

col1, col2 = st.columns([1, 7])

#col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Sectro P/FFO", value=sector_pffo)
    st.metric(label="Current P/FFO", value=current_pffo)
    st.metric(label="Mean P/FFO", value=mean_pffo)
    
with col2:
    fig, ax = plt.subplots()
    ax.plot(test_df)
    formatter = mdates.DateFormatter("%Y") ### formatter of the date
    locator = mdates.YearLocator()
    ax.xaxis.set_major_formatter(formatter) ## calling the formatter for the x-axis
    ax.xaxis.set_major_locator(locator) ## calling the locator for the x-axis
    st.pyplot(fig)

#with col3:
    

st.line_chart(test_df)
