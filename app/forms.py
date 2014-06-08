# coding=utf-8
from django import forms


class AddProductForm(forms.Form):
    """
    Formulaire permettant d'ajouter un produit à un frigo.
    Reprend les champs d'un produit (name, et expdate)
    ainsi que les champs de la table de liaison
    """
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    expdate = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    unit = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class AddFridgeForm(forms.Form):
    """
    Formulaire permettant d'ajouter un frigo.
    Reperendre les champs d'un frigo (owner et capacity)
    """
    owner = forms.CharField(max_length=100)
    capacity = forms.IntegerField()