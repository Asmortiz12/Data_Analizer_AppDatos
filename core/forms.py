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


class SelectCompanyForm(forms.Form):
    company_name = forms.ChoiceField(choices=[(c.COM_NAME, c.COM_NAME) for c in COMPANY.objects.all()])

class EditCompanyForm(forms.ModelForm):
    class Meta:
        model = COMPANY
        fields = ['COM_IMFORMATION', 'CON_IMAGE']  # Only include these fields
        widgets = {
            'COM_IMFORMATION': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['CON_IMAGE'].required = False 