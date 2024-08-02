from django.urls import path
from .views import HomeView, UpdateRecordsByDateView, export_to_excel, CompanyStockTransactionsView, edit_company

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('company/edit/', edit_company, name='edit_company'),
    path('update-records-by-date/', UpdateRecordsByDateView.as_view(), name='update_records_by_date'),
    path('exportar_excel/', export_to_excel, name='export_to_excel'),
    path('company-transactions/<str:company_name>/', CompanyStockTransactionsView.as_view(), name='company_stock_transactions'),
]