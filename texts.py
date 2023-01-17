texts_dict = {
    'intro': {
        'title': 'ريتات السعودية',
        'body': 'هذا الموقع هو ثمرة مشروع جانبي للحاجة الشخصية. جمعت فيه ما أظن أنه المقاييس المالية المهمة لتقييم لصناديق الاستثمار العقاري المتداولة في السعودية. قررت فيما بعد عرضها ونشرها للفائدة العامة. اختر صندوق من القائمة لتشاهد المقاييس المالية المتعلقة.',
    },
    'pffo': {
        'title': 'مكرر النقد من العمليات P/FFO',
        'body': 'أفضل طريقة للتعامل مع النصوص العربية بلغة بيثون هو استخدام الترميز يونيكود، التي يدعمها بيثون دعما أصليا، لا حاجة فيه إلى مكتبات خارجية أو دوال خاصة، وقد يكون هذا أهمّ ما دفعني لاختيار لغة بيثون، إذ يكفي أن تسبق النص بحرف يو u لتدع بيثون يريحك من عناء التفكير وبرمجة النصوص، ويعامل معها بشفافية عالية.',
    },
    'yield': {
        'title': 'عائد التوزيعات النقدية Dividend Yield',
        'body': 'أفضل طريقة للتعامل مع النصوص العربية بلغة بيثون هو استخدام الترميز يونيكود، التي يدعمها بيثون دعما أصليا، لا حاجة فيه إلى مكتبات خارجية أو دوال خاصة، وقد يكون هذا أهمّ ما دفعني لاختيار لغة بيثون، إذ يكفي أن تسبق النص بحرف يو u لتدع بيثون يريحك من عناء التفكير وبرمجة النصوص، ويعامل معها بشفافية عالية.',
    },
    'ffos': {
        'title': 'ربحية السهم من الأموال من العمليات FFO/Share',
        'body': 'عند تقييم الصناديق العقارية، تعتبر ربحية السهم من الأموال من العمليات البديل للمقياس المالي ربحية السهم Earnings Per Sahre (EPS) المعمول به عن تقييم الشركات. الصناديق العقارية الناجحة تزيد باستمرار من ربحية السهم من الأموال من العمليات مما يعطيها فرصة للتوسع وبالتالي دعم التوزيعات النقدية وارتفاع سعر السهم.',
    },
    'ffo_payout': {
        'title': 'نسبة التوزيعات النقدية إلى الأموال من العمليات FFO Payout Raito',
        'body': 'مقدار التوزيعات النقدية بالنسبة إلى الأموال من العمليات بدلاً من احتسابها بالنسبة إلى صافي الدخل كما هو معمول به في الشركات. بالنسبة للصناديق العقارية فإن الرقم المفضل هو أقل من 90%. زيادة النسبة بشكل مستمر تشير إلى أن التوزيعات تنمو بوتيرة أسرع من نمو الأموال من العمليات للصندوق.',
    },
}


def display_text(x, title_size=16, asis=False):
    
    global texts_dict
    
    if asis == True:
        text = texts_dict[x]
    
    else:
        text = '''
        <p style="direction: rtl; text-align: justify; font-size:{ts}px; font-weight: bold;">{title}</p>
        <p style="direction: rtl; text-align:justify">{body}</p>
        '''.format(
            ts = title_size,
            title = texts_dict[x]['title'],
            body = texts_dict[x]['body'])
    
    return text