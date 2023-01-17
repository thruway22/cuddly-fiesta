import streamlit as st

text_dict = {
    'pffo': {
        'en_title': 'P/FFO',
        'ar_title': 'مكرر النقد من العمليات',
        'body': 'أفضل طريقة للتعامل مع النصوص العربية بلغة بيثون هو استخدام الترميز يونيكود، التي يدعمها بيثون دعما أصليا، لا حاجة فيه إلى مكتبات خارجية أو دوال خاصة، وقد يكون هذا أهمّ ما دفعني لاختيار لغة بيثون، إذ يكفي أن تسبق النص بحرف يو u لتدع بيثون يريحك من عناء التفكير وبرمجة النصوص، ويعامل معها بشفافية عالية.',
    },
}

def display_text(metric):
    
    global text_dict
    
    text = '''
    <p style="direction: rtl; text-align: justify; font-size:16px; font-weight: bold;">{title}</p>
    <p style="direction: rtl; text-align:justify">{body}</p>
    '''.format(title = text_dict[metric]['ar_title']+' '+text_dict[metric]['en_title'],
               body = text_dict[metric]['body'])
    
    return st.markdown(text, unsafe_allow_html=True)
