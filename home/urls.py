
from django.urls import path
from .import views
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
    
]
