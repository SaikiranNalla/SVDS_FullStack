from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    class Meta:
        model = Order
        fields = [
            'date', 'from_address', 'to_address', 'consignor', 'consignee',
            'vehicle_number', 'vehicle_charge', 'value', 'packages', 'description',
            'eway_bill', 'consignment_invoice', 'actual_weight', 'charged_weight',
            'freight_charges'
        ]
        widgets = {field: forms.TextInput(attrs={'class': 'form-control'})
                   for field in fields if field != 'date'}
        widgets['description'] = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})