from django.contrib import admin
from django.urls import path
from sales.views import (
    DataRefreshView,
    RevenueAnalysisView,
    TopProductsView,
    CustomerAnalysisView
)

urlpatterns = [
    path('api/refresh_data/', DataRefreshView.as_view(), name='refresh-data'),
    path('api/revenue_analysis/', RevenueAnalysisView.as_view(), name='revenue-analysis'),
    path('api/top_products/', TopProductsView.as_view(), name='top-products'),
    path('api/customer_analysis/', CustomerAnalysisView.as_view(), name='customer-analysis'),
]