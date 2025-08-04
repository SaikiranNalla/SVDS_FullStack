from django import forms
from .models import Orders
from datetime import date


# might need signup form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# class OrderForm(forms.ModelForm):
#     date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
#     class Meta:
#         model = Orders
#         fields = [
#             'date', 'transit_from', 'transit_to', 'consignor', 'consignee',
#             'vehicle_number', 'vehicle_charge', 'consignment_value', 'packages', 'description',
#             'eway_bill', 'consignment_invoice', 'actual_weight', 'charged_weight',
#             'freight_charges'
#         ]
#         widgets = {field: forms.TextInput(attrs={'class': 'form-control'})
#                    for field in fields if field != 'date'}
#         widgets['description'] = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})


#
# class OrdersForm(forms.ModelForm):
#     # Override the date field to set today as the initial value
#     date = forms.DateField(
#         widget=forms.DateInput(
#             attrs={'type': 'date', 'class': 'form-control'}
#         ),
#         initial=date.today,
#         label="Transit Date"
#     )
#
#     class Meta:
#         model = Orders
#         fields = [
#             'date',
#             'vehicle_number', 'vehicle_charge',
#             'transit_from', 'transit_to',
#             'consignor', 'consignee',
#             'consignment_value', 'packages', 'description',
#             'eway_bill', 'consignment_invoice',
#             'actual_weight', 'charged_weight', 'freight_charges',
#             'delivery_status', 'payment_status',
#         ]
#         widgets = {
#             'vehicle_number':    forms.TextInput(attrs={'class': 'form-control'}),
#             'vehicle_charge':    forms.NumberInput(attrs={'class': 'form-control'}),
#             'transit_from':      forms.TextInput(attrs={'class': 'form-control'}),
#             'transit_to':        forms.TextInput(attrs={'class': 'form-control'}),
#             'consignor':         forms.TextInput(attrs={'class': 'form-control'}),
#             'consignee':         forms.TextInput(attrs={'class': 'form-control'}),
#             'consignment_value': forms.NumberInput(attrs={'class': 'form-control'}),
#             'packages':          forms.NumberInput(attrs={'class': 'form-control'}),
#             'description':       forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
#             'eway_bill':         forms.TextInput(attrs={'class': 'form-control'}),
#             'consignment_invoice': forms.TextInput(attrs={'class': 'form-control'}),
#             'actual_weight':     forms.NumberInput(attrs={'class': 'form-control'}),
#             'charged_weight':    forms.NumberInput(attrs={'class': 'form-control'}),
#             'freight_charges':   forms.NumberInput(attrs={'class': 'form-control'}),
#             # Django will render your choice fields as <select class="form-control">
#             'delivery_status':   forms.Select(attrs={'class': 'form-select'}),
#             'payment_status':    forms.Select(attrs={'class': 'form-select'}),
#         }



# orders/forms.py


class OrdersForm(forms.ModelForm):
    # 1) Override the date to default to today but remain editable
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=date.today,
        label="Transit Date"
    )

    # 2) Make other_charges a normal input
    other_charges = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        initial=0,
        label="Other Charges"
    )

    # 3) Make total_charge read‑only (we'll compute it in JS)
    total_charge = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        label="Total Charge"
    )

    class Meta:
        model = Orders
        fields = [
            # Vehicle Details
            'date', 'vehicle_number', 'vehicle_charge',

            # Consignment Details
            'transit_from', 'transit_to',
            'consignor', 'consignee',
            'consignment_value', 'packages', 'description',
            'eway_bill', 'consignment_invoice',
            'actual_weight', 'charged_weight', 'freight_charges',

            # Status & Billing
            # 'svds_bill_no', 'svds_bill_no'
            'delivery_status', 'payment_status',
            'other_charges', 'total_charge',
        ]
        widgets = {
            # Vehicle & numeric fields
            'vehicle_number':      forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_charge':      forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'transit_from':        forms.TextInput(attrs={'class': 'form-control'}),
            'transit_to':          forms.TextInput(attrs={'class': 'form-control'}),
            'consignor':           forms.TextInput(attrs={'class': 'form-control'}),
            'consignee':           forms.TextInput(attrs={'class': 'form-control'}),
            'consignment_value':   forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'packages':            forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'description':         forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'eway_bill':           forms.TextInput(attrs={'class': 'form-control'}),
            'consignment_invoice': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_weight':       forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'charged_weight':      forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'freight_charges':     forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),

            # Choice fields
            'delivery_status': forms.Select(attrs={'class': 'form-select'}),
            'payment_status':  forms.Select(attrs={'class': 'form-select'}),
        }
