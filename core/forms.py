from django import forms
from .models import COMPANY, PLACE_ORIGIN, TYPE_TRANSACTION, STOCK_TRANSACTION

class Company_Form(forms.Form):
    class meta:
        model  = COMPANY
        fields = '__all__'
        
        
class Place_Origin_Form(forms.Form):
    class meta:
        model  = PLACE_ORIGIN
        fields = '__all__'


class Type_Transaction_Form(forms.Form):
    class meta:
        model  = TYPE_TRANSACTION
        fields = '__all__'

        
class Stock_Transaction_Form(forms.Form):
    class meta:
        model  = STOCK_TRANSACTION
        fields = '__all__'
        


class UploadFileForm(forms.Form):
    excel = forms.FileField(label='Seleccionar archivo Excel')

