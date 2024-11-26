from django import forms
from .models import RegistroPesagem

class RegistroPesagemForm(forms.ModelForm):
    class Meta:
        model = RegistroPesagem
        fields = ['placa', 'numero_documento', 'imagem_entrada_upload', 'imagem_saida_upload']
