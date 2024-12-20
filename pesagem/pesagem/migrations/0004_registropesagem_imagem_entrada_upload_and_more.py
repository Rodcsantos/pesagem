# Generated by Django 5.1.3 on 2024-11-14 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesagem', '0003_alter_registropesagem_imagem_entrada_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registropesagem',
            name='imagem_entrada_upload',
            field=models.ImageField(blank=True, help_text='Imagem da entrada (upload manual)', null=True, upload_to='imagens/entrada_manual/'),
        ),
        migrations.AddField(
            model_name='registropesagem',
            name='imagem_saida_upload',
            field=models.ImageField(blank=True, help_text='Imagem da saída (upload manual)', null=True, upload_to='imagens/saida_manual/'),
        ),
        migrations.AlterField(
            model_name='registropesagem',
            name='imagem_entrada',
            field=models.TextField(blank=True, help_text='Imagem da entrada (em base64)', null=True),
        ),
        migrations.AlterField(
            model_name='registropesagem',
            name='imagem_saida',
            field=models.TextField(blank=True, help_text='Imagem da saída (em base64)', null=True),
        ),
    ]
