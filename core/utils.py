import os
import zipfile
import pandas as pd
from datetime import datetime
from django.core.files.storage import default_storage
from .models import COMPANY, PLACE_ORIGIN, TYPE_TRANSACTION, STOCK_TRANSACTION

def process_excel_file(excel_file):
    df = pd.read_excel(excel_file)
    return df

def save_stock_transactions_from_df(df):
    for index, row in df.iterrows():
        print(f"Procesando fila {index}: {row}")
        company_id = row['Company ID']
        company_name = row['Company']
        company_ruc = row['Ruc']
        print(f"CompanyId:{company_id}, Empresa: {company_name}, RUC: {company_ruc}")

        company, created = COMPANY.objects.get_or_create(
            COM_NAME=company_name,
            defaults={'COM_ID': company_id, 'COM_RUC': company_ruc, 'COM_SYMBOL': row['Symbol']}
        )
        print(f"Empresa creada: {company}")

        place_origin, created = PLACE_ORIGIN.objects.get_or_create(
            OR_LOCATION=row['place origin']
        )
        print(f"Lugar de origen creado: {place_origin}")

        type_transaction, created = TYPE_TRANSACTION.objects.get_or_create(
            TYT_Type=row['type_transaction']
        )
        print(f"Tipo de transacción creado: {type_transaction}")

        stock_transaction = STOCK_TRANSACTION(
            COM_ID=company,
            OR_ID=place_origin,
            TYT_ID=type_transaction,
            STT_DATE=row['date'],
            STT_DESCRIPTION=row['Decripition'],
            STT_NOMINAL_VALUE=row['Nominal Value'],
            STT_PRICE=row['price'],
            STT_NUM_SHARES=row['Number Shares'],
            STT_CASH_VALUE=row['Cash value']
        )
        print(f"Transacción de acciones creada: {stock_transaction}")
        stock_transaction.save()

def filter_dataframe_by_date(df, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    df['date'] = pd.to_datetime(df['date'])
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df_filtered

def associate_company_logos():
    zip_file_path = default_storage.path('CompanyLogos.zip')
    temp_dir = default_storage.path('temp/CompanyLogos/')
    
    # Ensure the temp directory exists
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        company_id, _ = os.path.splitext(file)
                        try:
                            company = COMPANY.objects.get(COM_ID=company_id)
                            image_path = os.path.join(root, file)
                            with open(image_path, 'rb') as image_file:
                                company.CON_IMAGE.save(file, image_file, save=True)
                        except COMPANY.DoesNotExist:
                            print(f"Company with ID '{company_id}' not found.")
    
    finally:
        # Clean up temporary files
        delete_directory(temp_dir)

def delete_directory(path):
    """Recursively delete a directory and its contents."""
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

