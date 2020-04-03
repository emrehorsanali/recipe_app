from django import forms


class RecipeRateForm(forms.Form):
    rate = forms.IntegerField()
