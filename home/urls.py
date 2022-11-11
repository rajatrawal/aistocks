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
    path('predictTomorrow',views.predict_tomorrow,name='predit_tomorrow'),
    path('companyInfo',views.company_info,name='company_info'),
    path('getFinancialData',views.get_financial_data,name='get_financial_data'),
    path('getSignals',views.get_signals,name='get_signals'),
    path('getStock/<str:symbol_name>',views.get_stock,name='get_stock'),
    path('table/<str:type>',views.get_table,name='get_table'),
    path('chart/<str:symbol>',views.chart,name='chart'),
    path('signals',views.get_signals,name='signals'),
    path('aboutUs',views.about_us,name='about_us'),
    path('sitemap.xml', sitemap,{'sitemaps': {'ticker': GenericSitemap(info_dict, priority=0.5,changefreq='never')}},
        name='django.contrib.sitemaps.views.sitemap'),
    
]
