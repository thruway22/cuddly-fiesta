import streamlit as st
from backend import *

# hide the stupid zoom button on charts
st.markdown('''<style> button[title="View fullscreen"] {visibility: hidden;}
            button[title="View fullscreen"]:hover {visibility: hidden;}</styles>''',
            unsafe_allow_html=True)

tickers = {    
    #9999: '',
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

st.markdown(display_text(
            body=texts.loc['main_body'].value, title=texts.loc['main_title'].value, title_size=24),
            unsafe_allow_html=True)

ticker = st.selectbox('Choose fund', tickers.keys(), label_visibility='collapsed') #,
             #format_func=lambda x:tickers[x])

##################################

fdata = pd.read_csv('data/fdata.csv')
fdata[year_col] = pd.to_datetime(fdata[year_col], format='%Y-%m-%d')
fdata = fdata.sort_values(by=year_col)

tickers_dict = {fdata.ticker.unique()[i]: \
                str(fdata.ticker.unique()[i]) + ': ' + fdata.name.unique()[i] \
                for i in range(len(fdata.ticker.unique()))}

pdata = get_historical_prices(tickers_dict)
ticker_data = get_ticker_data(fdata, pdata, ticker)
sector_data = get_sector_data(fdata, pdata, tickers_dict)
yoy, hoh = get_categorical_data(fdata, ticker)

##################################




st.pyplot(chart_timeseries_data(ticker_data, sector_data, 'price', relative_plot=True))
st.pyplot(chart_categorical_data(yoy, hoh, 'asset', 'yoy', True))
      
     
           
            
