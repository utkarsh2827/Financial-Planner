from django.urls import path
from . import views
from .views import (
    PortfolioListView,
    StockDetailView,
    StockUpdateView,
    StockDeleteView
)    
urlpatterns = [
    path('', views.home, name = 'financial_planner-home'),
    path('analysis/<str:symbol>/<str:name>', views.stock_analysis_page, name = 'financial_planner-home'),
    path('portfolio/', PortfolioListView.as_view(), name = 'financial_planner-portfolio-list'),
    path('fsearch/', views.fund_search, name = 'financial_planner-fund-search'),
    path('port_opt/', views.recommend, name = 'portfolio_opt'),
    path('optimise/', views.port_opt, name = 'ajax'),
    path('stock/<int:pk>/', StockDetailView.as_view(), name = 'stock-detail'),
    path('about/', views.about, name = 'financial_planner-about'),
    path('search/', views.stock_search, name = 'financial_planner-stock-search'),
    path('stock/<str:symbol>/<str:name>/<str:choice>',views.stock_create,name = 'stock-create'),
    path('stock/<int:pk>/update/', StockUpdateView.as_view(), name = 'stock-update'),
    path('stock/<int:pk>/delete/', StockDeleteView.as_view(), name = 'stock-delete'),
   
]