import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime  
from datetime import timedelta
from pandas.tseries.offsets import DateOffset
from pandas.tseries.offsets import MonthEnd
from eod import EodHistoricalData
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
nav_col = 'nav'
asset_col='asset'
equity_col='equity'
casti_col='casti'
debt_col='debt'

fdata = pd.read_csv('data/fdata.csv')
fdata[year_col] = pd.to_datetime(fdata[year_col], format='%Y-%m-%d')
fdata = fdata.sort_values(by=year_col)

tickers_dict = {fdata.ticker.unique()[i]: \
                str(fdata.ticker.unique()[i]) + ': ' + fdata.name.unique()[i] \
                for i in range(len(fdata.ticker.unique()))}

# st.cache() ############################### UPDATE
def get_historical_prices(tickers_dict):
    api_key = st.secrets['api_key']
    client = EodHistoricalData(api_key)
    resp = client.get_prices_eod('4330.SR', period='d', order='a', from_='2018-01-01')
    df = pd.DataFrame(resp)[['date']]
    
    for i in tickers_dict.keys():
        resp = client.get_prices_eod(str(i)+'.SR', period='d', order='a', from_='2018-01-01')
        df = df.merge(pd.DataFrame(resp)[['date', 'adjusted_close']].rename(columns={"adjusted_close": i}),
                 on='date', how='left')
        
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        
    return df
  
pdata = get_historical_prices(tickers_dict)

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
    
    global pdata
    global fdata
    
    '''pdata -> df1 and fdata -> df2'''
    
    # get historical prices for input ticker
    df1 = pdata[['date',str(ticker)]].rename(columns = {str(ticker):'price'})
    
    # get historical financials for input ticker
    df2 = fdata[[ticker_col, year_col, shares_col, ffo_col, dividend_col, nav_col]]
    
    # rolling agg on metrics for input ticker to obtain Trailing-12-Months (TTM) values
    df2 = df2[df2[ticker_col]==ticker].set_index(year_col).rolling(2).agg(
        {shares_col:'mean', ffo_col:'sum', dividend_col:'sum', nav_col:'mean'}).reset_index()
    
    df2 = df2.rename(columns = {year_col:'period_end'})
    
    # DateOffset to subtract 6 months from period_end
    # MonthEnd to roll forward to the end of the given (0) month
    df2['period_start'] = df2['period_end'] - DateOffset(months=6) + MonthEnd(0)
    
    
    '''output df'''
    
    # start with a copy of df1 as the base for output df
    df = df1.copy()
    
    # merge metrcis to prices as per proper date range
    df[shares_col] = rock_and_roll(df1, df2, shares_col)
    df[ffo_col] = rock_and_roll(df1, df2, ffo_col)
    df[dividend_col] = rock_and_roll(df1, df2, dividend_col)
    df[nav_col] = rock_and_roll(df1, df2, nav_col)
    
    # forward fill data
    df = df.set_index('date').fillna(method='ffill').dropna()
    
    # compute output metrics
    df['yield'] = 100 * (abs(df[dividend_col]) / df[shares_col]) / df['price']
    df['pffo'] = (df['price'] * df[shares_col]) / df[ffo_col]
    df['navpd'] = ((df['price'] / df[nav_col]) - 1) * 100    
    
    # take only needed columns
    df = df[['price', nav_col, 'navpd', 'yield', 'pffo']] 
    
    return df
  
# cached ############################
def get_sector_data(yield_col='yield', pffo_col='pffo'):
    
    global pdata
    global tickers_dict
    
    df = pdata[['date']].set_index('date')
    df_yield = df.copy() 
    df_pffo = df.copy() 
    
    for i in tickers_dict.keys():
        df_aux = get_ticker_data(i)
        df_yield[i] = df_aux[yield_col]
        df_pffo[i] = df_aux[pffo_col]
        
    df[yield_col] = df_yield.median(axis=1)
    df[pffo_col] = df_pffo.median(axis=1)
        
    return df
  
def chart_timeseries_data(metric_col, relative_plot=False):
    
    global ticker_data
    global sector_data
    
    # set defult font and colors
    plt.rcParams['font.size'] = 8
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['text.color'] = "262730"
    plt.rcParams['xtick.color'] = '262730'
    
    var_dict = {
        'figsize': {
            'price': (6.4, 1.4),
            'nav': (6.4, 1.4),
            'navpd': (6.4, 1.4),
            'yield': (6.4, 1.4),
            'pffo': (6.4, 1.4),
        },
        'linewidth': {
            'price': 1,
            'nav': 1,
            'navpd': 0,
            'yield': 1,
            'pffo': 1,  
        },
        'unit': {
            'price': '{value:0.2f} SAR',
            'nav': '{value:0.2f} SAR',
            'navpd': '{value:0.2f}%',
            'yield': '{value:0.2f}%',
            'pffo': '{value:0.2f}x',
        },
        'relative_plot': {
            'price': ticker_data['nav'],
            'yield': sector_data['yield'],
            'pffo': sector_data['pffo']
        },
    }
    
    linewidth = 0 if metric_col == 'navpd' else 1
    
    fig, ax = plt.subplots(
        figsize=var_dict['figsize'][metric_col])
    
    ax.plot(ticker_data[metric_col], color='#0068c9', alpha=1,
            linewidth=var_dict['linewidth'][metric_col])
        
    # format datetime on xaxis
    formatter = mdates.DateFormatter("%Y")
    locator = mdates.YearLocator()
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(locator)
    
    # get coordinates of current/last point (year, value)
    x = ticker_data[metric_col].tail(1).index[0]
    y = ticker_data[metric_col][-1]
    
    # add a bit of a margin to right a-axis
    ax.set_xlim(right= x + timedelta(days=330))
    
    # mark current value on chart, cord:(year, last point)
    ax.plot(x, y, color='#f63366', **{'marker': '.'})

    # annotate current value on chart, cord:()
    plt.annotate(var_dict['unit'][metric_col].format(value=y),
             xy=(x, y), xytext=(7, -3), size=10,
             xycoords=('data', 'data'), textcoords='offset points',
             bbox=dict(boxstyle="round, pad=0.3", fc="#0068c9", lw=0, alpha=0.10))
    
    if relative_plot == True:
        ax.plot(var_dict['relative_plot'][metric_col],
                linewidth=1, color='#0068c9', alpha=0.2)
        
        # get coordinates of current/last point (year, value)
        '''x2 = var_dict['relative_plot'][metric_col].tail(1).index[0]
        y2 = var_dict['relative_plot'][metric_col][-1]
        ax.plot(x2, y2, color='#09ab3b', **{'marker': '.'})
        # annotate current value on chart, cord:()
        plt.annotate(var_dict['unit'][metric_col].format(value=y2),
                 xy=(x2, y2), xytext=(7, -3), 
                 xycoords=('data', 'data'), textcoords='offset points',
                 bbox=dict(boxstyle="round, pad=0.3", fc="#f0f2f6", lw=0))'''
        
        
    if metric_col == 'navpd':
        x_curve = ticker_data[metric_col].index
        y_curve = ticker_data[metric_col].values
        ax.fill_between(x_curve, y_curve,
                        where=(y_curve > 0), color='#ff2b2b', alpha=0.15)
        ax.fill_between(x_curve, y_curve,
                        where=(y_curve < 0), color='#09ab3b', alpha=0.15)
        
        #ax.get_yaxis().set_visible(True)
    
    # hide y-axis
    ax.get_yaxis().set_visible(False)
    
    # hide framebox
    plt.box(False)
        
    #plt.show()
    return fig
  
def compute_metrics(df):
    df['ffos'] = df[ffo_col] / df[shares_col]
    df['ffo_payout'] = 100 * abs(df[dividend_col]) / df[ffo_col]
    df['roic'] = 100 * df[ebit_col] / (df[equity_col] + df[debt_col])
    df['op_margin'] = 100 * df[ebit_col] / df[revenue_col]
    df['net_debt_ebitda'] = (df[debt_col] - df[casti_col]) / df[ebitda_col]
    #df['net_debt_capital'] = (df[debt_col] - df[casti_col]) / (df[equity_col] + df[debt_col])
    df['coverage'] = df[ebit_col] / abs(df[interest_col])
    
    # replace inf by zero
    # those with zero net_debt will get inf when computing metrics
    df.replace([np.inf, -np.inf], 0, inplace=True)
    
    return df
  
def get_categorical_data(ticker):
    
    global fdata
    
    # create yoy and ttm for input ticker
    hoh = fdata[fdata[ticker_col] == ticker].drop(columns=[ticker_col, name_col])    
    df_aux1 = hoh.copy()
    df_aux2 = hoh.copy()
    
    # hoh
    hoh = compute_metrics(hoh)
    hoh['date_y'] = hoh[year_col].dt.year
    hoh['date_m'] = hoh[year_col].dt.month
    hoh['period'] = hoh['date_y'].astype(str) + '-' + hoh['date_m'].astype(str)
    hoh = hoh.set_index('period').drop(columns =['date_y', 'date_m', 'year'])
    
    
    # check if each year has 2 fiscal halfs to produce agg for full fiscal year
    df_aux1[year_col] = df_aux1[year_col].dt.year
    df_aux1 = df_aux1[df_aux1.duplicated(year_col, keep=False) == True]
    
    # group by year
    df_aux1 = df_aux1.groupby(year_col).agg({
        shares_col: 'mean',
        ffo_col: 'sum',
        dividend_col: 'sum',
        revenue_col: 'sum',
        interest_col: 'sum',
        ebitda_col: 'sum',
        ebit_col: 'sum',
        nav_col: 'last',
        asset_col: 'last',
        equity_col: 'last',
        casti_col: 'last',
        debt_col: 'last',
    })
    
    # roll by last 2 fiscal halfs
    df_aux2 = df_aux2.rolling(2).agg({
        shares_col: 'mean',
        ffo_col: 'sum',
        dividend_col: 'sum',
        revenue_col: 'sum',
        interest_col: 'sum',
        ebitda_col: 'sum',
        ebit_col: 'sum',
        nav_col: 'mean',
        asset_col: 'mean',
        equity_col: 'mean',
        casti_col: 'mean',
        debt_col: 'mean',
    }).tail(1)
    
    #ttm = ttm.rename(index={0: 'TTM'})
    df_aux2['indx'] = 'TTM'
    df_aux2 = df_aux2.set_index('indx')
        
    # concat to create output df and compute metrics
    yoy = pd.concat([df_aux1, df_aux2])
    yoy = compute_metrics(yoy)    
    
    return yoy, hoh
  
def chart_categorical_data(metric_col, method='yoy', show_change=False):
    
    global yoy
    global hoh
    
    var_dict = {
        'unit': {
            'revenue': '%.1fM', 
            'asset': '%.1fM',
            'ffos': '%.2f',
            'ffo_payout': '%.1f%%',
            'roic': '%.1f%%',
            'op_margin': '%.1f%%',
            'net_debt_ebitda': '%.2fx',
            'coverage': '%.2fx',
        }
    }
    
    # get df
    df = yoy.copy() if method == 'yoy' else hoh.copy()
    df = df.dropna()
        
    # set x and y axis data
    x = df.index
    y = df[metric_col]
    
    if metric_col == 'revenue' or metric_col == 'asset':
        y = df[metric_col] / 1000000
    
    # set defult font and colors
    plt.rcParams['font.size'] = 8
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['text.color'] = "262730"
    #plt.rcParams['axes.labelcolor'] = 'ffffff'
    plt.rcParams['xtick.color'] = '262730'
    
    # create object
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 5 if show_change == True else 4.5),
                                   height_ratios=[1 if show_change == True else 0, 4], sharex=True)
    bars = ax2.bar(np.arange(len(x)), y, tick_label=x, color='#0068c9', width=0.96)

    # show bar values on top
    ax2.bar_label(bars, size=10,
                 padding=6, fmt=var_dict['unit'][metric_col],
                 bbox=dict(boxstyle="round, pad=0.3", fc="#0068c9", lw=0, alpha=0.10))
    
    if show_change == True:        
        # add chnage% by shifting metric_col and then computing
        df['shift'] = df[metric_col].shift(1)
        df['change'] = 100 * (df[metric_col] - df['shift']) / abs(df['shift'])
        changes = df['change'].fillna(0)
        
        y.plot(ax=ax1, kind='line', color='#edeef1')
        
        line = ax1.lines[0]
        for x, y, c in zip(line.get_xdata(), line.get_ydata(), changes):
            
            if c == 0:
                bbox_color = '#f0f2f6'
            elif c >= 0:
                bbox_color = '#DEF0E2'
            else:
                bbox_color = '#F9E0DE'
                
            #bbox_color = '#f0f2f6' is c == 0 else '#DEF0E2' if c>=0 else '#F9E0DE'
            ax1.annotate('{:.1f}%'.format(c),
                         (x, y), xytext=(0, 0), size=8,
                         textcoords="offset points",
                         ha='center', va='center',
                         bbox=dict(boxstyle="round, pad=0.3", fc=bbox_color, lw=0))
    
    
    # hide y-axis
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    
    
    # hide framebox
    ax1.set_frame_on(False)
    ax2.set_frame_on(False)
    
    # remove side (x) margins and pad (y) 
    plt.margins(x=0, y=0.15)
    
    plt.subplots_adjust(hspace= -0.1 if show_change == True else 0)
    
    #plt.show()
    return fig
  
##################################################
##################################################

texts = pd.read_csv('data/texts.csv', encoding='utf8', index_col='id')
  
def display_text(title=None, title_size=16, **bodies):
    
    output = ''
    
    if title != None:
        output = output + f'<p style="direction: rtl; text-align: justify; font-size:{title_size}px; font-weight: bold;">{title}</p>'
        
    for body in bodies.values():
        output = output + f'<p style="direction: rtl; text-align:justify">{body}</p>'
        
    return output