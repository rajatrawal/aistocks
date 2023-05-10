from django.contrib.sitemaps.views import sitemap
from django.urls import path
from .import views
from django.contrib.sitemaps import GenericSitemap
from .models import Ticker

info_dict = {
    'queryset': Ticker.objects.order_by('symbol'),

}


urlpatterns = [

    path('',views.index,name='index'),
    path('predictAjaxTomorrow',views.predict_ajax_tomorrow,name='predit_ajax_tomorrow'),
    path('companyAjaxInfo',views.company_ajax_info,name='company_ajax_info'),
    path('getFinancialAjaxData',views.get_financial_ajax_data,name='get_financial_ajax_data'),
    path('getTicker/<str:symbol_name>',views.get_ticker,name='get_ticker'),
    path('table/<str:type>',views.get_table,name='get_table'),
    path('chart/<str:symbol>',views.chart,name='chart'),
    path('signals',views.get_signals,name='signals'),
    path('aboutUs',views.about_us,name='about_us'),
    path('getMarqueeTagAjaxData',views.get_marquee_tag_ajax_data,name='get_marquee_tag_ajax_data'),
    path('getIndexAjaxData',views.get_index_ajax_data,name='get_index_ajax_data'),
    path('getSecondaryIndexAjaxData',views.get_secondary_index_ajax_data,name='get_secondary_index_ajax_data'),
    
    path('sitemap.xml', sitemap,{'sitemaps': {'ticker': GenericSitemap(info_dict, priority=0.5,changefreq='never')}},
        name='django.contrib.sitemaps.views.sitemap'),
    
]
