from django import forms
from .models import Stock, Funds
class StockCreationForm(forms.ModelForm):

    class Meta:
        model = Stock
        fields = ['quantity_owned']

class FundsCreationForm(forms.ModelForm):

    class Meta:
        model = Funds
        fields = ['quantity_owned']