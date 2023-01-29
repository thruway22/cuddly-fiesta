import streamlit as st
from utilities import *

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css('style.css')

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
#last_update = pdata.tail(1)['date'].values[0]
pdata['date'] = pd.to_datetime(pdata['date'], format='%Y-%m-%d')

fdata = pd.read_csv('data/fdata.csv')
fdata[year_col] = pd.to_datetime(fdata[year_col], format='%Y-%m-%d')
fdata = fdata.sort_values(by=year_col)

tickers_dict = {fdata.ticker.unique()[i]: \
                str(fdata.ticker.unique()[i]) + ': ' + fdata.name.unique()[i] \
                for i in range(len(fdata.ticker.unique()))}

sector_data = get_sector_data(fdata, pdata, tickers_dict)

texts = pd.read_csv('data/texts.csv', encoding='utf8', index_col='id')
  
def display_text(**kwargs):
    
    '''
    takes title, header, body, footnote
    '''
     
    global texts
    
    output = ''
    for i in kwargs.keys():
        output += f'<p id="{i}">{texts.loc[kwargs[i]].value}</p>'
                
    return st.markdown(output, unsafe_allow_html=True)

def display_divider():
    return st.markdown('<hr/>', unsafe_allow_html=True)

def display_metric(metric1, metric1_fmt, metric1_label,
                   metric2, metric2_fmt, metric2_label,
                   metric3, metric3_fmt, metric3_label):
     fmt_dict = {
         'currency': ' SAR',
         'percent': '%',
         'multiple': 'x'
     }   
     output = f'''<div id="metric_block">
                  <p id="metric_value">{metric1:.2f}{fmt_dict[metric1_fmt]}</p>
                  <p id="metric_label">{texts.loc[metric1_label].value}</p>
                  <p id="metric_value">{metric2:.2f}{fmt_dict[metric2_fmt]}</p>
                  <p id="metric_label">{texts.loc[metric2_label].value}</p>
                  <p id="metric_value">{metric3:.2f}{fmt_dict[metric3_fmt]}</p>
                  <p id="metric_label">{texts.loc[metric3_label].value}</p>
                  </div>'''
     return st.markdown(output, unsafe_allow_html=True)

def display_chart(kind, metric_col,
                  ts_relative_plot=None, ct_method='yoy', ct_show_change=True):
    global ticker_data
    global sector_data
    global yoy
    global hoh
    if kind == 'ts':
        return st.pyplot(chart_timeseries_data(ticker_data, sector_data, metric_col, ts_relative_plot))
    if kind == 'ct':
        return st.pyplot(chart_categorical_data(yoy, hoh, metric_col, ct_method, ct_show_change))

display_text(title='intro_title', body='intro_body')
ticker = st.selectbox('Choose fund', tickers.keys(), label_visibility='collapsed', format_func=lambda x:tickers[x])
display_divider()

placeholder = st.empty()

if ticker == 9999:
    pass
else:
    ticker_data = get_ticker_data(fdata, pdata, ticker)
    yoy, hoh = get_categorical_data(fdata, ticker)
             
    with placeholder.container():
        display_text(header='price_header', body='price_body')
        display_metric(ticker_data['navpd'][-1], 'percent', 'pd_label',
                       ticker_data['nav'][-1], 'currency', 'nav_label',
                       ticker_data['price'][-1], 'currency', 'price_label')
        display_chart('ts', 'price')
        
        display_divider()
        tab01, tab02 = st.tabs(['مقارنة بوسيط القطاع الحالي', 'مقارنة بوسيط الصندوق التاريخي'])
        with tab01:
            display_text(header='yield_header', body='yield_body')
            display_metric(((ticker_data.tail(1)['yield'][0] / sector_data.tail(1)['yield'][0]) - 1) * 100 , 'percent', 'pd_label',
                           sector_data.tail(1)['yield'][0], 'percent', 'sector_yield_label',
                           ticker_data.tail(1)['yield'][0], 'percent', 'ticker_yield_label')
            display_chart('ts', 'yield', ts_relative_plot='sector')
        
        with tab02:
            display_text(header='yield_header', body='yield_body')
            display_metric(((ticker_data.tail(1)['yield'][0] / ticker_data['yield'].median()) - 1) * 100 , 'percent', 'pd_label',
                           ticker_data['yield'].median(), 'percent', 'sector_yield_label',
                           ticker_data.tail(1)['yield'][0], 'percent', 'ticker_yield_label')
            display_chart('ts', 'yield', ts_relative_plot='ticker')
        
        display_divider()
        tab03, tab04 = st.tabs(['مقارنة بوسيط القطاع الحالي', 'مقارنة بوسيط الصندوق التاريخي'])
        with tab03:
            display_text(header='pffo_header', body='pffo_body')
            display_metric(((ticker_data.tail(1)['pffo'][0] / sector_data.tail(1)['pffo'][0]) - 1) * 100 , 'percent', 'pd_label',
                           sector_data.tail(1)['pffo'][0], 'multiple', 'sector_pffo_label',
                           ticker_data.tail(1)['pffo'][0], 'multiple', 'ticker_pffo_label')
            display_chart('ts', 'pffo', ts_relative_plot='sector')
            
        with tab04:
            display_text(header='pffo_header', body='pffo_body')
            display_metric(((ticker_data.tail(1)['pffo'][0] / ticker_data['pffo'].median()) - 1) * 100 , 'percent', 'pd_label',
                           ticker_data['pffo'].median(), 'multiple', 'sector_pffo_label',
                           ticker_data.tail(1)['pffo'][0], 'multiple', 'ticker_pffo_label')
            display_chart('ts', 'pffo', ts_relative_plot='ticker')
        
        # ct_method='yoy'
        col11, col12 = st.columns(2)
        with col11:
            display_divider()
            tab05, tab06 = st.tabs(['سنوي', 'نصفي'])
            with tab05:            
                display_chart('ct', 'ffos')
                display_text(header='ffos_header', body='ffos_body')
            with tab06:            
                display_chart('ct', 'ffos', ct_method='yoy')
                display_text(header='ffos_header', body='ffos_body')
        with col12:
            display_divider()
            tab07, tab08 = st.tabs(['سنوي', 'نصفي'])
            with tab07:
                display_chart('ct', 'ffo_payout')
                display_text(header='ffo_payout_header', body='ffo_payout_body')
            with tab08:
                display_chart('ct', 'ffo_payout', ct_method='yoy')
                display_text(header='ffo_payout_header', body='ffo_payout_body')
            
        col21, col22 = st.columns(2)
        with col21:
            display_divider()
            display_chart('ct', 'asset')
            display_text(header='asset_header', body='asset_body')
        with col22:
            display_divider()
            display_chart('ct', 'revenue')
            display_text(header='revenue_header', body='revenue_body')
            

        col31, col32 = st.columns(2)
        with col31:
            display_divider()
            display_chart('ct', 'roic')
            display_text(header='roic_header', body='roic_body')
        with col32:
            display_divider()
            display_chart('ct', 'op_margin')
            display_text(header='op_margin_header', body='op_margin_body')
            
        col41, col42 = st.columns(2)
        with col41:
            display_divider()
            display_chart('ct', 'net_debt_ebitda')
            display_text(header='net_debt_ebitda_header', body='net_debt_ebitda_body')
        with col42:
            display_divider()
            display_chart('ct', 'coverage')
            display_text(header='coverage_header', body='coverage_body')
            
        display_divider()
        display_text(footnote='footnote')
            
            
            
      
     
           
            
