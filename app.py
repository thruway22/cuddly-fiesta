import streamlit as st
from utilities import *

# hide the stupid zoom button on charts
st.markdown('''<style> button[title="View fullscreen"] {visibility: hidden;}
            button[title="View fullscreen"]:hover {visibility: hidden;}</styles>''',
            unsafe_allow_html=True)

tickers = {    
    9999: '',
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


def display_chart(kind, metric_col,
                  ts_relative_plot=False, ct_method='yoy', ct_show_change=True):
    global ticker_data
    global sector_data
    global yoy
    global hoh
    if kind == 'ts':
        return st.pyplot(chart_timeseries_data(ticker_data, sector_data, metric_col, ts_relative_plot))
    if kind == 'ct':
        return st.pyplot(chart_categorical_data(yoy, hoh, metric_col, ct_method, ct_show_change))

st.markdown(display_text(
            body=texts.loc['main_body'].value, title=texts.loc['main_title'].value, title_size=24),
            unsafe_allow_html=True)

ticker = st.selectbox('Choose fund', tickers.keys(), label_visibility='collapsed', format_func=lambda x:tickers[x])

placeholder = st.empty()

if ticker == 9999:
    pass
else:
    ticker_data = get_ticker_data(fdata, pdata, ticker)
    yoy, hoh = get_categorical_data(fdata, ticker)
            
    with placeholder.container():
            display_chart('ts', 'price', ts_relative_plot=True)
            display_chart('ct', 'asset')
            
      
     
           
            
