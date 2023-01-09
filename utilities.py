import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime  
from datetime import timedelta

def prepare_data(file_path):
    
    '''
    reads the source csv file and compute metrics
    
    Args:
    file_path (str): 
    
    Return:
    df (pd.DataFrame):
    '''
    
    # read data
    df = pd.read_csv(file_path)
    
    # compute metrics
    df['pffo'] = round((df.price * df.shares) / df.ffo, 2)
    df['ffos'] = round(df.ffo / df.shares, 2)
    df['ffo_payout'] = round(100 * -df.dividend / df.ffo, 2) # %
    df['roic'] = round(100 * df.ebit / (df.equity + df.debt), 2) # %
    df['op_margin'] = round(100 * df.ebit / df.revenue, 2) # %
    df['net_debt_ebitda'] = round((df.debt - df.casti) / df.ebitda, 2)
    df['net_debt_capital'] = round((df.debt - df.casti) / (df.equity + df.debt), 2)
    df['coverage'] = round(df.ebit / -df.interest, 2)
    
    # replace inf by zero
    # those with zero net_debt will get inf when computing metrics
    df.replace([np.inf, -np.inf], 0, inplace=True)
    
    return df
  
  
def compute_pffo(df, price_col='price', shares_col='shares', ffo_col='ffo'):
    '''
    helper function takes any df with required columns and compute pffo
    
    Args:
    df (str):
    price_col, shares_col, ffo_col (str): column names
    
    Return:
    df (pd.DataFrame):
    '''
    
    df['pffo'] = (df[price_col] * df[shares_col]) / df[ffo_col]
    df = df[['pffo']]
    
    return df
  

def get_sector_pffo(df, ticker_col='ticker', year_col='year', shares_col='shares', ffo_col='ffo'):
    '''
    gets the current/latest market prices of each ticker and compute pffo
    for each ticker as per latest announced ffo 
    
    Args:
    df (str):
    ticker_col, year_col (str): column names
    
    Return:
    df (pd.DataFrame):
    '''
    
    # get only last ffo from input df and set index to ticker
    df = df[df[year_col] == df[year_col].max()].set_index(ticker_col)
    
    # filter out unnecessary columns
    df = df[[shares_col, ffo_col]]
    
    # get current prices
    price_list = []
    
    for i in df.index:
        price = round(yf.Ticker(str(i)+'.SR').history(period='1d', interval='1d')['Close'][0], 2)
        price_list.append(price)
    
    # add to df
    df['price'] = price_list
    
    # compute pff
    df = compute_pffo(df)
    
    return round(df.median()[0], 2)
  
  
def get_ticker_pffo(df, ticker, ticker_col='ticker', year_col='year', shares_col='shares', ffo_col='ffo'):
    '''
    gets the current/latest market prices of each ticker and compute pffo
    for each ticker as per latest announced ffo 
    
    Args:
    df (str):
    ticker_col, year_col (str): column names
    
    Return:
    df (pd.DataFrame):
    '''
    
    # (1) get histrocal pffo
    
    # Concat to produce correct ticker format
    ticker_adj = str(ticker)+".SR"
    
    # get aux dataframe
    df = df[df[ticker_col]==ticker][[year_col, shares_col, ffo_col]]
    df[year_col] = pd.to_datetime(df[year_col], format='%Y')
    
    # get prices
    df_prices = yf.Ticker(ticker_adj).history(period='5y', interval='1d', actions=False)
    
    # select only close col and rest index
    df_prices = df_prices[['Close']].reset_index()
    
    # merge
    df_output = pd.merge(df_prices, df,
                         left_on = df_prices['Date'].apply(lambda x: (x.year)),
                         right_on = df[year_col].apply(lambda y: (y.year)),
                         how = 'left')
    
    # change date (needed?)
    df_output['Date'] = df_output['Date'].dt.date
    
    # take only needed columns, set index, fillna
    df_output = df_output[['Date', 'Close', shares_col, ffo_col]].set_index('Date').fillna(method='ffill')
    
    df_output = compute_pffo(df_output, price_col='Close')
    
    ########
    
    # (2) get current pffo
    #current_pffo = round(df_output.tail(1)['pffo'][0], 2)
    
    # (3) get median pffo
    #median_pffo = round(df_output.median()[0], 2)
    
    return df_output
  
  
def chart_pffo(ticker, file_path='data.csv'):
    
    # prepare data
    df = prepare_data(file_path)
    sector_pffo = get_sector_pffo(df)
    ticker_pffo = get_ticker_pffo(df, ticker)
    
    # set defult font and colors
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['text.color'] = "262730"
    plt.rcParams['ytick.color'] = '262730'
    plt.rcParams['xtick.color'] = '262730'
        
    # create objects
    fig, ax = plt.subplots()
    ax.plot(ticker_pffo, linewidth=1, color='lightgrey')
    
    # format datetime on xaxis
    formatter = mdates.DateFormatter("%Y")
    locator = mdates.YearLocator()
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(locator)
    
    # plt.style.use('default')
    
    # get coordinates of current/last point (year, value)
    x = ticker_pffo.tail(1).index[0]
    y = ticker_pffo['pffo'][-1]
    
    # mark current value on chart, cord:(year, last point)
    ax.plot(x, y, color='#f63366', **{'marker': '.'})

    # annotate current value on chart, cord:()
    plt.annotate('%0.2f' % y, xy=(x, y), xytext=(6, -3), 
                 xycoords=('data', 'data'), textcoords='offset points',
                 bbox=dict(boxstyle="round, pad=0.3", fc="#f0f2f6", lw=0))


    # draw horizontal line for fund median and annotate value
    ticker_median = ticker_pffo['pffo'].median()
    ax.axhline(ticker_median, color='#0068c9', linewidth=0.5, xmin=0.03, xmax=0.97)

    plt.annotate('Fund Median %0.2f' % ticker_median, xy=(0, ticker_median), xytext=(10, -3), 
                 xycoords=('axes fraction', 'data'), textcoords='offset points',
                 bbox=dict(boxstyle="round, pad=0.3", fc="#f0f2f6", lw=0))
    
    # draw horizontal line for sector median and annotate value
    ax.axhline(sector_pffo, color='#0068c9', linewidth=0.5, xmin=0.03, xmax=0.97)

    plt.annotate('Sector Median %0.2f' % sector_pffo, xy=(0, sector_pffo), xytext=(10, -3), 
                 xycoords=('axes fraction', 'data'), textcoords='offset points',
                 bbox=dict(boxstyle="round, pad=0.3", fc="#f0f2f6", lw=0))
    
    # add a bit of a margin to right a-axis
    ax.set_xlim(right= x + timedelta(days=300))
    
    # add a bit of margin to top y-axis
    ax.set_ylim(top=ax.get_ylim()[1]+2)
    
    # hide framebox
    plt.box(False)
    
    plt.show()
    
    
def chart_metric(df, ticker, metric_col, ticker_col='ticker', year_col='year'):

    # prepare data
    df = df[df[ticker_col]==ticker][[year_col, metric_col]].sort_values(by=[year_col])

    # set x and y axis data
    x = df[year_col].apply(str)
    y = df[metric_col]

    # set defult font and colors
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['text.color'] = "262730"
    #plt.rcParams['axes.labelcolor'] = 'ffffff'
    plt.rcParams['xtick.color'] = '262730'

    # create object
    fig, ax = plt.subplots()
    bars = ax.bar(x, y, color='#0068c9')

    # hide y-axis
    ax.get_yaxis().set_visible(False)

    # show bar values on top
    ax.bar_label(bars)

    # remove side margins
    plt.margins(x=0)

    # hide framebox
    plt.box(False)

    plt.show
