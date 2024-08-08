from django.urls import path
from .views import HomeView, ImportRecordsByDateView, export_to_excel, CompanyStockTransactionsView
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('import-records-by-date/', ImportRecordsByDateView.as_view(), name='import_records_by_date'),
    path('exportar_excel/', export_to_excel, name='export_to_excel'),
    path('company-transactions/<str:company_name>/', CompanyStockTransactionsView.as_view(), name='company_stock_transactions'),
]