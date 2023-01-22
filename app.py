import streamlit as st
from utilities import *

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css('style.css')

tickers = {    
    #9999: '',
    4330: '4330: Riyad REIT الرياض ريت',
    4331: '4331: Aljazira REIT الجزيرة ريت',
    4332: '4332: Jadwa REIT Alharamain جدوى ريت الحرمين',
    4333: '4333: Taleem REIT تعليم ريت',
    4334: '4334: Almaather REIT المعذر ريت',
    4335: '4335: Musharaka REIT مشاركة ريت',
    4336: '4336: Mulkia Gulf REIT ملكية الخليج ريت',
    4337: '4337: SICO Saudi REIT سيكو السعودية ريت',
    4338: '4338: Alahli REIT الأهلي ريت',
    4339: '4339: Derayah REIT دراية ريت',
    4340: '4340: Alrajhi REIT الراجحي ريت',
    4342: '4342: Jadwa REIT جدوى ريت',
    4344: '4344: SEDCO Capital REIT سدكو كابيتال ريت',
    4345: '4345: Alinma Retail REIT الإنماء ريت التجزئة',
    4346: '4346: MEFIC REIT ميفك ريت',
    4347: '4347: Bonyan REIT بنيان ريت',
    4348: '4348: Alkhabeer REIT الخبير ريت'
}

pdata = pd.read_csv('data/pdata.csv')
pdata['date'] = pd.to_datetime(pdata['date'], format='%Y-%m-%d')

fdata = pd.read_csv('data/fdata.csv')
fdata[year_col] = pd.to_datetime(fdata[year_col], format='%Y-%m-%d')
fdata = fdata.sort_values(by=year_col)

tickers_dict = {fdata.ticker.unique()[i]: \
                str(fdata.ticker.unique()[i]) + ': ' + fdata.name.unique()[i] \
                for i in range(len(fdata.ticker.unique()))}

sector_data = get_sector_data(fdata, pdata, tickers_dict)

texts = pd.read_csv('data/texts.csv', encoding='utf8', index_col='id')
  
def display_text(title=None, body=None, title_size=16, **extra_bodies):
    global texts
    output = ''
    if title != None:
        output = output + f'<p id="title">{texts.loc[title].value}</p>'
    if body !=None:
        output = output + f'<p style="direction: rtl; text-align:justify">{texts.loc[body].value}</p>'               
    for extra_body in extra_bodies.values():
        output = output + f'<p style="direction: rtl; text-align:justify">{texts.loc[extra_body].value}</p>'
    return st.markdown(output, unsafe_allow_html=True)

def display_divider():
    return st.markdown('<hr />', unsafe_allow_html=True)

def display_metric(ticker_metric, sector_metric, fmt):
     fmt_dict = {'p': '%', 'm': 'x'} #style="direction: rtl; text-align:center"    
     output = f'''<div id="metric_block"><p id="metric_value">{ticker_metric:.2f}{fmt_dict[fmt]}</p>
                  <p id="metric_label">{texts.loc['ticker_label'].value}</p>
                  <p id="metric_value">{sector_metric:.2f}{fmt_dict[fmt]}</p>
                  <p id="metric_label">{texts.loc['sector_label'].value}</p></div>'''
     return st.markdown(output, unsafe_allow_html=True)

def display_chart(kind, metric_col,
                  ts_relative_plot=True, ct_method='yoy', ct_show_change=True):
    global ticker_data
    global sector_data
    global yoy
    global hoh
    if kind == 'ts':
        return st.pyplot(chart_timeseries_data(ticker_data, sector_data, metric_col, ts_relative_plot))
    if kind == 'ct':
        return st.pyplot(chart_categorical_data(yoy, hoh, metric_col, ct_method, ct_show_change))

display_text('intro_title', 'intro_body', 24)

ticker = st.selectbox('Choose fund', tickers.keys(), label_visibility='collapsed', format_func=lambda x:tickers[x])

placeholder = st.empty()

if ticker == 9999:
    pass
else:
    ticker_data = get_ticker_data(fdata, pdata, ticker)
    yoy, hoh = get_categorical_data(fdata, ticker)
            
    ticker_yield = ticker_data['yield'].median()
    ticker_pffo = ticker_data['pffo'].median()

    sector_yield = sector_data.tail(1)['yield'][0]
    sector_pffo = sector_data.tail(1)['pffo'][0]
            
    with placeholder.container():
            display_text('price_title', 'price_body')
            display_chart('ts', 'price')
            display_chart('ts', 'navpd', ts_relative_plot=False)
            display_divider()
            display_metric(ticker_yield, sector_yield, 'p')
            display_chart('ts', 'yield')
            display_divider()
            display_metric(ticker_pffo, sector_pffo, 'm')
            display_chart('ts', 'pffo')
            display_divider()
            
      
     
           
            
