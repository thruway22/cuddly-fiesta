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

# global data columns
ticker_col = 'ticker'
year_col = 'year'
name_col='name'
shares_col='shares'
ffo_col='ffo'
dividend_col='dividend'
revenue_col='revenue'
interest_col='interest'
ebitda_col='ebitda'
ebit_col='ebit'
asset_col='asset'
equity_col='equity'
casti_col='casti'
debt_col='debt'
######


data = pd.read_csv('data_hy.csv')
data[year_col] = pd.to_datetime(data[year_col], format='%Y-%m-%d')
data = data.sort_values(by=year_col)

tickers_dict = {data.ticker.unique()[i]: \
                str(data.ticker.unique()[i]) + ': ' + data.name.unique()[i] \
                for i in range(len(data.ticker.unique()))}

def rock_and_roll(df1, df2, df2_metric_col,
                  df1_date_col='date',
                  df2_start_col='period_start',
                  df2_end_col='period_end'):
    
    # yahoo finance does not keep historical data for some tickers
    # but only returns the most recent 1D data
    # check if ticker has only 1D data point, if true
    # return the most recent metric value to allow output metrics to computed 
    if len(df1) == 1:
        values = df2.tail(1)[df2_metric_col].values
    
    # check date range in df1 and return appropriate metric value from df2
    else:
        values = np.piecewise(np.zeros(len(df1)),
                    [(df1[df1_date_col].values >= start_date) & (df1[df1_date_col].values < end_date) \
                    for start_date, end_date in zip(df2[df2_start_col].values, df2[df2_end_col].values)],
                    np.append(df2[df2_metric_col].values, np.nan))

    return values
  

def get_ticker_data(ticker):
    '''
    gets the current/latest market prices of each ticker and compute pffo
    for each ticker as per latest announced ffo 
    
    Args:
    data (pd.DataFrame):
    ticker_col, year_col (str): column names
    
    Return:
    df (pd.DataFrame):
    '''
    
    #### df1 : prices dataframe ####
    
    # get historical prices for input ticker
    df1 = yf.Ticker(str(ticker)+".SR").history(
        start='2018-01-01', interval='1d', actions=False)[['Close']]
    
    # reset index to prepare for merge and rename columns just because OCD
    df1 = df1.reset_index().rename(columns = {'Close':'price', 'Date':'date'})
    
    # get only the date from the timestamp and format
    df1['date'] = df1['date'].dt.date
    df1['date'] = pd.to_datetime(df1['date'], format='%Y-%m-%d')
    
    ### df2 : metrics dataframe ###
    
    global data
    df2 = data[[ticker_col, year_col, shares_col, ffo_col, dividend_col]]
    
    # rolling agg on metrics for input ticker to obtain Trailing-12-Months (TTM) values
    df2 = df2[df2[ticker_col]==ticker].set_index(year_col).rolling(2).agg(
        {shares_col:'mean', ffo_col:'sum', dividend_col:'sum'}).reset_index()
    
    df2 = df2.rename(columns = {year_col:'period_end'})
    
    # DateOffset to subtract 6 months from period_end
    # MonthEnd to roll forward to the end of the given (0) month
    df2['period_start'] = df2['period_end'] - DateOffset(months=6) + MonthEnd(0)
    
    ### output df ###
    
    # start with a copy of df1 as the base for output df
    df = df1.copy()
    
    # merge metrcis to prices as per proper date range
    df[shares_col] = rock_and_roll(df1, df2, shares_col)
    df[ffo_col] = rock_and_roll(df1, df2, ffo_col)
    df[dividend_col] = rock_and_roll(df1, df2, dividend_col)
    
    # forward fill data
    df = df.set_index('date').fillna(method='ffill').dropna()
    
    # compute output metrics
    df['yield'] = 100 * (abs(df[dividend_col]) / df[shares_col]) / df['price']
    df['pffo'] = (df['price'] * df[shares_col]) / df[ffo_col]
    
    # take only needed columns
    df = df[['price', 'yield', 'pffo']]
    
    return df
  

@st.cache(ttl=21600)
def get_sector_data(price_col='price',
                    yield_col='yield',
                    pffo_col='pffo'):
    
    global data
    global tickers_dict
    
    # create empty df with designated columns
    df = pd.DataFrame({'yield': [], 'pffo': []})
    
    for i in tickers_dict.keys():
        df.loc[i] = [get_ticker_data(i)[['yield']].median()[0],
                     get_ticker_data(i)[['pffo']].median()[0]]
        
    return df
  
sector_data = get_sector_data()

def chart_timeseries_data(ticker, metric_col):
    
    # set defult font and colors
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['text.color'] = "262730"
    plt.rcParams['ytick.color'] = '262730'
    plt.rcParams['xtick.color'] = '262730'
    
    # get asked metric
    ticker_data = get_ticker_data(ticker)[[metric_col]]
        
    metric_dict = {
        'figsize': {
            'price': (6.4, 1.4),
            'yield': (6.4, 1.4),
            'pffo': (6.4, 1.4),
        },
        'unit': {
            'price': '{value:0.2f} SAR',
            'yield': '{value:0.2f}%',
            'pffo': '{value:0.2f}x',
        },
    }
    
    # create objects
    fig, ax = plt.subplots(figsize=metric_dict['figsize'][metric_col])
    ax.plot(ticker_data, linewidth=1, color='lightgrey')
    
    # format datetime on xaxis
    formatter = mdates.DateFormatter("%Y")
    locator = mdates.YearLocator()
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(locator)
    
    # get coordinates of current/last point (year, value)
    x = ticker_data.tail(1).index[0]
    y = ticker_data[metric_col][-1]
    
    # add a bit of a margin to right a-axis
    ax.set_xlim(right= x + timedelta(days=330))
    
    if len(ticker_data) == 1:
        
        ax.get_xaxis().set_visible(False)
        
        plt.annotate(metric_dict['unit'][metric_col].format(value=y),
                     xy=(0.5, 0.8), xycoords="axes fraction", va="center", ha="center",
                     bbox=dict(boxstyle="round, pad=0.3", fc="#f0f2f6", lw=0))
        
        plt.annotate('Current Value',
                     xy=(0.5, 0.6), xycoords="axes fraction", va="center", ha="center")
        
        plt.annotate('No historical data on Yahoo! Finance for this fund.', size=8,
                     xy=(0.5, 0.2), xycoords="axes fraction", va="center", ha="center")
                
    else:
        # mark current value on chart, cord:(year, last point)
        ax.plot(x, y, color='#f63366', **{'marker': '.'})

        # annotate current value on chart, cord:()
        plt.annotate(metric_dict['unit'][metric_col].format(value=y),
                 xy=(x, y), xytext=(7, -3), 
                 xycoords=('data', 'data'), textcoords='offset points',
                 bbox=dict(boxstyle="round, pad=0.3", fc="#f0f2f6", lw=0))
    
    if metric_col != 'price':
        # draw horizontal line for sector median and annotate value
        global sector_data
        sector_median = sector_data[metric_col].median()
        sector_median = metric_dict['unit'][metric_col].format(value=sector_median)
        
        plt.annotate('Sector Current Median',
                     xy=(0.25, 1.15), xycoords="axes fraction", va="center", ha="center")

        plt.annotate(sector_median,
                     xy=(0.25, 1.35), xycoords="axes fraction", va="center", ha="center",
                     bbox=dict(boxstyle="round, pad=0.3", fc="#f0f2f6", lw=0))
    
        # draw horizontal line for fund median and annotate value
        ticker_median = ticker_data[metric_col].median()
        ticker_median = metric_dict['unit'][metric_col].format(value=ticker_median)
        ticker_median = 'NM' if len(ticker_data) == 1 else ticker_median
        
        plt.annotate('Fund Historical Median',
                     xy=(0.75, 1.15), xycoords="axes fraction", va="center", ha="center")

        plt.annotate(ticker_median,
                     xy=(0.75, 1.35), xycoords="axes fraction", va="center", ha="center",
                     bbox=dict(boxstyle="round, pad=0.3", fc="#f0f2f6", lw=0))
    
    # hide y-axis
    ax.get_yaxis().set_visible(False)
    
    # hide framebox
    plt.box(False)
    
    #plt.tight_layout()
    
    #plt.show()
    return fig
  
  
def get_categorical_data(ticker):
    
    global data
    
    # create yoy and ttm for input ticker
    yoy = ttm = data[data[ticker_col] == ticker].drop(columns=[ticker_col, name_col])
        
    # check if each year has 2 fiscal halfs to produce agg for full fiscal year
    yoy[year_col] = yoy[year_col].dt.year
    yoy = yoy[yoy.duplicated(year_col, keep=False) == True]
    
    # group by year
    yoy = yoy.groupby(year_col).agg({
        shares_col: 'mean',
        ffo_col: 'sum',
        dividend_col: 'sum',
        revenue_col: 'sum',
        interest_col: 'sum',
        ebitda_col: 'sum',
        ebit_col: 'sum',
        asset_col: 'last',
        equity_col: 'last',
        casti_col: 'last',
        debt_col: 'last',
    })
    
    # roll by last 2 fiscal halfs
    ttm = ttm.rolling(2).agg({
        shares_col: 'mean',
        ffo_col: 'sum',
        dividend_col: 'sum',
        revenue_col: 'sum',
        interest_col: 'sum',
        ebitda_col: 'sum',
        ebit_col: 'sum',
        asset_col: 'mean',
        equity_col: 'mean',
        casti_col: 'mean',
        debt_col: 'mean',
    }).tail(1)
    
    #ttm = ttm.rename(index={0: 'TTM'})
    ttm['indx'] = 'TTM'
    ttm = ttm.set_index('indx')
        
    # concat to create output df and compute metrics
    df = pd.concat([yoy, ttm])
    
    df['ffos'] = df[ffo_col] / df[shares_col]
    df['ffo_payout'] = 100 * abs(df[dividend_col]) / df[ffo_col]
    df['roic'] = 100 * df[ebit_col] / (df[equity_col] + df[debt_col])
    df['op_margin'] = 100 * df[ebit_col] / df[revenue_col]
    df['net_debt_ebitda'] = (df[debt_col] - df[casti_col]) / df[ebitda_col]
    df['net_debt_capital'] = (df[debt_col] - df[casti_col]) / (df[equity_col] + df[debt_col])
    df['coverage'] = df[ebit_col] / abs(df[interest_col])
    
    # replace inf by zero
    # those with zero net_debt will get inf when computing metrics
    df.replace([np.inf, -np.inf], 0, inplace=True)
    
    return df
  
  
def chart_categorical_data(ticker, metric_col):
    
    # get df
    df = get_categorical_data(ticker)
    
    # add chnage% by shifting metric_col and then computing
    df['shift'] = df[metric_col].shift(1)
    df['chnage'] = 100 * (df[metric_col] - df['shift']) / abs(df['shift'])
    
    # set x and y axis data
    x = df.index
    y = df[metric_col]
    
    # set chnages
    chnages = df['chnage']
    
    # set defult font and colors
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['text.color'] = "262730"
    #plt.rcParams['axes.labelcolor'] = 'ffffff'
    plt.rcParams['xtick.color'] = '262730'
    
    # create object
    fig, ax = plt.subplots()
    bars = ax.bar(np.arange(len(x)), y, tick_label=x, color='#0068c9', width=0.96)

    # hide y-axis
    ax.get_yaxis().set_visible(False)

    # show bar values on top
    ax.bar_label(bars, padding=16, fmt='%.2f',
                bbox=dict(boxstyle="round, pad=0.3", fc="#f0f2f6", lw=0))
    # fmt='%g%%'
    
    # annotate chnage% by looping over bars
    for bar, c in zip(bars.patches, chnages):
        
        if bar.get_height() >=0:
            y_xytext = 6
        else:
            y_xytext = -6 
        
        # set color and value based on chnage direction
        if np.isnan(c) or np.isinf(c):
            c_color = 'grey'
            c='NM'
        elif c>=0:
            c_color = 'green'
            c='%.0f%%' % c
        else:
            c_color = 'red'
            c='%.0f%%' % c
        
        plt.annotate(c,
                     (bar.get_x() + bar.get_width() / 2, bar.get_height()), #(x,y) cord
                     ha='center', va='center',
                     xytext=(0, y_xytext), textcoords='offset points',
                     size=8, color=c_color)

    # remove side (x) margins and pad (y) 
    plt.margins(x=0, y=0.15)
    
    # hide framebox
    plt.box(False)
    
    #plt.show()
    return fig
  
  
texts = pd.read_csv('texts.csv', encoding='utf8', index_col='id')
  
def display_text(title=None, title_size=16, **bodies):
    
    output = ''
    
    if title != None:
        output = output + f'<p style="direction: rtl; text-align: justify; font-size:{title_size}px; font-weight: bold;">{title}</p>'
        
    for body in bodies.values():
        output = output + f'<p style="direction: rtl; text-align:justify">{body}</p>'
        
    return output
