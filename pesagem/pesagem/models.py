from django.db import models
from django.utils import timezone

class RegistroPesagem(models.Model):
    placa = models.CharField(max_length=10, help_text="Placa do veículo")
    numero_documento = models.CharField(max_length=50, help_text="Número da NF ou contêiner")
    
    peso_entrada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Peso de entrada (kg)")
    data_entrada = models.DateTimeField(null=True, blank=True, help_text="Data e hora da entrada")
    imagem_entrada = models.TextField(null=True, blank=True, help_text="Imagem da entrada (em base64)")
    imagem_entrada_upload = models.ImageField(upload_to='imagens/entrada_manual/', null=True, blank=True, help_text="Imagem da entrada (upload manual)")

    peso_saida = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Peso de saída (kg)")
    data_saida = models.DateTimeField(null=True, blank=True, help_text="Data e hora da saída")
    imagem_saida = models.TextField(null=True, blank=True, help_text="Imagem da saída (em base64)")
    imagem_saida_upload = models.ImageField(upload_to='imagens/saida_manual/', null=True, blank=True, help_text="Imagem da saída (upload manual)")

    def save(self, *args, **kwargs):
        if self.peso_entrada is not None and self.data_entrada is None:
            self.data_entrada = timezone.now()

        if self.peso_saida is not None and self.data_saida is None:
            self.data_saida = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        entrada = f"{self.peso_entrada} kg - {self.data_entrada}" if self.data_entrada else "Entrada não registrada"
        saida = f"{self.peso_saida} kg - {self.data_saida}" if self.data_saida else "Saída não registrada"
        return f"{self.placa} | Entrada: {entrada} | Saída: {saida}"
