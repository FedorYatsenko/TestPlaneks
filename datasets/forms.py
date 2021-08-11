from django import forms

from .models import DataSchema, SchemaColumn, Dataset


from django.forms.models import inlineformset_factory

ColumnFormset = inlineformset_factory(
    DataSchema, SchemaColumn,
    fields=('order', 'name', 'data_type'),
    extra=0,
    can_delete=False,
    widgets={
        'order': forms.NumberInput(attrs={
            'required': True,
            'readonly': True,
            'value': 1,
            'class': 'form-control'
        }),
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'required': True
        }),
        'data_type': forms.Select(attrs={
            'class': 'form-select',
            'required': True
        }),
    },
    min_num=1
)


class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['count', 'delimiter', 'quote_char']

        widgets = {
            'count': forms.NumberInput(attrs={
                'required': True,
                'class': 'form-control',
                'min': 1,
                'max': 100000
            }),
            'delimiter': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'quote_char': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }
