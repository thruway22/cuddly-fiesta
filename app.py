import streamlit as st
from utilities import *

# hide the stupid zoom button on charts
st.markdown('''<style> button[title="View fullscreen"] {visibility: hidden;}
            button[title="View fullscreen"]:hover {visibility: hidden;}</styles>''',
            unsafe_allow_html=True)

tickers = {    
    9999: '',
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

ticker = st.selectbox('Choose fund', tickers.keys(), label_visibility='collapsed',
             format_func=lambda x:tickers[x])

placeholder = st.empty()

if ticker == 9999:
    pass
else:
    with placeholder.container():
        
        st.pyplot(chart_timeseries_data(ticker, 'price'))
        
        st.markdown('<hr />', unsafe_allow_html=True)
        st.markdown(display_text(
            body=texts.loc['yield_body'].value, title=texts.loc['yield_title'].value), 
                    unsafe_allow_html=True)
        st.pyplot(chart_timeseries_data(ticker, 'yield'))
        
        st.markdown('<hr />', unsafe_allow_html=True)
        st.markdown(display_text(
            body=texts.loc['pffo_body'].value, title=texts.loc['pffo_title'].value), 
                    unsafe_allow_html=True)
        st.pyplot(chart_timeseries_data(ticker, 'pffo'))
      
        col1a, col2a = st.columns(2)

        with col1a:
            hoh, yoy = st.tabs(["سنوي", "نصف سنوي"])
            #st.markdown('<hr />', unsafe_allow_html=True)
            st.markdown(display_text(
                body=texts.loc['ffos_body'].value, title=texts.loc['ffos_title'].value), 
                        unsafe_allow_html=True)
            with hoh:          
                        st.pyplot(chart_categorical_data(ticker, 'ffos'))
            with yoy:
                        st.pyplot(chart_categorical_data(ticker, 'ffo'))
                
        with col2a:
            st.markdown('<p style="direction: rtl; text-align:center">تجربة</p>', unsafe_allow_html=True)
            #st.markdown('<hr />', unsafe_allow_html=True)
            st.markdown(display_text(
                body=texts.loc['ffo_payout_body'].value, title=texts.loc['ffo_payout_title'].value), 
                        unsafe_allow_html=True)
            st.pyplot(chart_categorical_data(ticker, 'ffo_payout'))
            
        col1b, col2b = st.columns(2)

        with col1b:
            st.markdown('<hr />', unsafe_allow_html=True)
            st.write('net_debt_ebitda')
            st.markdown(display_text(
                body=texts.loc['ffos_body'].value, title=texts.loc['ffos_title'].value), 
                        unsafe_allow_html=True)
            st.pyplot(chart_categorical_data(ticker, 'net_debt_ebitda'))
                
            st.markdown('<hr />', unsafe_allow_html=True)
            st.write('coverage')
            st.markdown(display_text(
                body=texts.loc['ffo_payout_body'].value, title=texts.loc['ffo_payout_title'].value), 
                        unsafe_allow_html=True)
            st.pyplot(chart_categorical_data(ticker, 'coverage'))
            
        with col1b:
            st.markdown('<hr />', unsafe_allow_html=True)
            st.markdown(display_text(
                body=texts.loc['ffos_body'].value, title=texts.loc['ffos_title'].value), 
                        unsafe_allow_html=True)
            st.pyplot(chart_categorical_data(ticker, 'dividend'))
                
        with col2b:
            st.markdown('<hr />', unsafe_allow_html=True)
            st.write('rev')
            st.markdown(display_text(
                body=texts.loc['ffo_payout_body'].value, title=texts.loc['ffo_payout_title'].value), 
                        unsafe_allow_html=True)
            st.pyplot(chart_categorical_data(ticker, 'revenue'))
            
            st.markdown('<hr />', unsafe_allow_html=True)
            st.write('asset')
            st.markdown(display_text(
                body=texts.loc['ffo_payout_body'].value, title=texts.loc['ffo_payout_title'].value), 
                        unsafe_allow_html=True)
            st.pyplot(chart_categorical_data(ticker, 'asset'))
           
            
