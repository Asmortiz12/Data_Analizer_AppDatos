from django.shortcuts import render,  get_object_or_404, redirect
from django.views.generic import TemplateView
from .forms import UploadFileForm
import pandas as pd
from django.http import HttpResponse
from openpyxl import Workbook
from .models import COMPANY, PLACE_ORIGIN, TYPE_TRANSACTION, STOCK_TRANSACTION
import plotly.graph_objs as go
from plotly.offline import plot
from django.conf import settings
from django.core.files.storage import default_storage
import os
from datetime import datetime
from django.db.models import Max, Min, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.core.exceptions import ValidationError
from .utils import process_excel_file, save_stock_transactions_from_df, filter_dataframe_by_date, associate_company_logos
from datetime import datetime
from decimal import Decimal
from .chart import (generate_candlestick_chart, generate_macd_chart, generate_rsi_chart,
                     generate_sma_chart, generate_volume_chart, generate_projection_chart)
from .calculations import (calculate_ohlc, calculate_macd, calculate_rsi,
                           calculate_sma, calculate_general_summary)
import zipfile
from django.contrib import messages



class HomeView(TemplateView):
    template_name = "home.html"


def companies_processor(request):
    search_query = request.GET.get('search', '')
    if search_query:
        companies = COMPANY.objects.filter(
            COM_NAME__icontains=search_query).order_by('COM_NAME')
    else:
        companies = COMPANY.objects.all().order_by('COM_NAME')
    return {
        'companies': companies,
        'search_query': search_query
    }



class ImportRecordsByDateView(TemplateView):
    template_name = "import_records_by_date.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        error = False
        alert_message = None

        if "excel" in request.FILES:
            try:
                excel_file = request.FILES["excel"]
                df = process_excel_file(excel_file)

                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')

                if start_date and end_date:
                    df_filtered = filter_dataframe_by_date(df, start_date, end_date)
                    save_stock_transactions_from_df(df_filtered)

                    # Asociar logos de compañías
                    try:
                        associate_company_logos()
                        alert_message = "Data and logos imported successfully"
                    except Exception as e:
                        alert_message = f"Data imported but an error occurred while associating logos: {str(e)}"
                        error = True

                else:
                    alert_message = "Please provide a valid date range."
                    error = True

            except Exception as e:
                alert_message = f"An error occurred while importing data: {str(e)}"
                error = True
                print(f"Error during import: {e}")

        return render(request, self.template_name, {
            "alert_message": alert_message,
            "error": error,
        })





def export_to_excel(request):
    # Recuperar los datos de la base de datos
    data = list(STOCK_TRANSACTION.objects.all().values())

    # Obtener todos los IDs únicos de compañías, lugares de origen y tipos de transacciones
    company_ids = set(row['COM_ID_id'] for row in data)
    origin_ids = set(row['OR_ID_id'] for row in data)
    transaction_type_ids = set(row['TYT_ID_id'] for row in data)

    # Cargar todos los nombres correspondientes de las compañías, lugares de origen y tipos de transacciones
    companies = {company.COM_ID: company.COM_NAME for company in COMPANY.objects.filter(
        COM_ID__in=company_ids)}
    origins = {origin.OR_ID: origin.OR_LOCATION for origin in PLACE_ORIGIN.objects.filter(
        OR_ID__in=origin_ids)}
    transaction_types = {transaction.TYT_ID: transaction.TYT_Type for transaction in TYPE_TRANSACTION.objects.filter(
        TYT_ID__in=transaction_type_ids)}

    # Actualizar los valores en el data con los nombres correspondientes
    for row in data:
        row['COM_ID_id'] = companies.get(row['COM_ID_id'])
        row['OR_ID_id'] = origins.get(row['OR_ID_id'])
        row['TYT_ID_id'] = transaction_types.get(row['TYT_ID_id'])

    # Crear un DataFrame con los datos actualizados
    df = pd.DataFrame(data)

    # Convertir la fecha a un formato legible
    df['STT_DATE'] = pd.to_datetime(df['STT_DATE']).dt.strftime('%d/%m/%Y')

    # Crear un archivo Excel desde el DataFrame
    excel_file = df.to_excel('datos_exportados.xlsx', index=False)

    # Leer el archivo Excel y devolverlo como respuesta
    with open('datos_exportados.xlsx', 'rb') as excel:
        response = HttpResponse(excel.read(
        ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=datos_exportados.xlsx'
        return response


class CompanyStockTransactionsView(TemplateView):
    template_name = "datos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_name = self.kwargs.get('company_name')
        sort_by = self.request.GET.get('sort_by', 'STT_DATE')
        order = self.request.GET.get('order', 'desc')

        # Obtener las fechas de inicio y fin del filtro
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        company = get_object_or_404(COMPANY, COM_NAME=company_name)
        
        # Obtener todas las transacciones para determinar el rango completo de fechas
        all_transactions = STOCK_TRANSACTION.objects.filter(COM_ID=company)
        first_record_date = all_transactions.aggregate(Min('STT_DATE'))['STT_DATE__min']
        last_record_date = all_transactions.aggregate(Max('STT_DATE'))['STT_DATE__max']

        # Filtrar por rango de fechas si se proporcionan
        filtered_transactions = all_transactions
        if start_date and end_date:
            try:
                filtered_transactions = filtered_transactions.filter(STT_DATE__range=[start_date, end_date])
            except ValidationError:
                pass  # Si ocurre un error, no aplicar filtro
        elif start_date:
            try:
                filtered_transactions = filtered_transactions.filter(STT_DATE__gte=start_date)
            except ValidationError:
                pass  # Si ocurre un error, no aplicar filtro
        elif end_date:
            try:
                filtered_transactions = filtered_transactions.filter(STT_DATE__lte=end_date)
            except ValidationError:
                pass  # Si ocurre un error, no aplicar filtro

        # Convertir a DataFrame y formatear fechas
        df = pd.DataFrame(list(filtered_transactions.values()))
        df['STT_DATE'] = pd.to_datetime(df['STT_DATE']).dt.strftime('%Y-%m-%d')

        # Ordenar por la columna seleccionada
        if sort_by in df.columns:
            df.sort_values(by=sort_by, inplace=True, ascending=(order == 'asc'))

        ohlc_df = calculate_ohlc(df)
        ohlc_df = calculate_macd(ohlc_df)
        ohlc_df = calculate_rsi(ohlc_df)
        ohlc_df = calculate_sma(ohlc_df)

        # Generar gráficos
        candlestick_div = generate_candlestick_chart(ohlc_df)
        macd_div = generate_macd_chart(ohlc_df)
        rsi_div = generate_rsi_chart(ohlc_df)
        sma_div = generate_sma_chart(ohlc_df)
        volume_div = generate_volume_chart(ohlc_df)

        # Obtener las últimas medias móviles calculadas
        sma_values = {
            'SMA_100': ohlc_df['SMA_100'].dropna().values[-10:],
            'SMA_200': ohlc_df['SMA_200'].dropna().values[-10:],
            'SMA_300': ohlc_df['SMA_300'].dropna().values[-10:]
        }

        
        projected_dates = pd.date_range(start=ohlc_df['STT_DATE'].iloc[-1], periods=11, freq='D')[1:]
        projection_div = generate_projection_chart(projected_dates, sma_values['SMA_100'])

        general_summary = {
            'total_transactions': filtered_transactions.count(),
            'total_shares': filtered_transactions.aggregate(Sum('STT_NUM_SHARES'))['STT_NUM_SHARES__sum'] or 0,
            'highest_price': filtered_transactions.aggregate(Max('STT_PRICE'))['STT_PRICE__max'] or 0,
            'lowest_price': filtered_transactions.aggregate(Min('STT_PRICE'))['STT_PRICE__min'] or 0,
            'total_value': filtered_transactions.aggregate(Sum('STT_CASH_VALUE'))['STT_CASH_VALUE__sum'] or 0,
        }

        # Asegurarse de que las fechas se formateen correctamente para la visualización
        formatted_first_record_date = first_record_date.strftime('%Y-%m-%d') if first_record_date else 'No records'
        formatted_last_record_date = last_record_date.strftime('%Y-%m-%d') if last_record_date else 'No records'

        context.update({
            "transactions": df.to_dict('records'),
            "company": company,
            "candlestick_div": candlestick_div,
            "macd_div": macd_div,
            "rsi_div": rsi_div,
            "volume_div": volume_div,
            "sma_div": sma_div,
            "projection_div": projection_div,
            "order": order,
            "sort_by": sort_by,
            "general_summary": general_summary,
            "start_date": start_date,
            "end_date": end_date,
            "first_record_date": formatted_first_record_date,
            "last_record_date": formatted_last_record_date,
            "recently_edited_info": {
                'company_name': company.COM_NAME,
                'information': company.COM_IMFORMATION or 'No additional information'
            }
        })

        return context

