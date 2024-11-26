# pesagem/urls.py
from django.urls import path
from . import views, camera

app_name = 'pesagem'  # Adicionando o namespace aqui

urlpatterns = [
    path('registrar/', views.registrar_pesagem, name='registrar_pesagem'),
    path('sucesso/', views.pesagem_sucesso, name='pesagem_sucesso'),  # Adicione essa linha
    path('video_feed/', camera.video_feed, name='video_feed'),
    path('pesagens/pendentes/', views.listar_pesagens_pendentes, name='listar_pesagens_pendentes'),
    path('pesagens/registrar_saida/<int:id>/', views.registrar_peso_saida, name='registrar_peso_saida'),
    path('pesagens/realizadas/', views.listar_pesagens_realizadas, name='listar_pesagens_realizadas'),  # Nova URL para listar pesagens realizadas
    path('pesagens/gerar_pdf/<int:id>/', views.gerar_pdf, name='gerar_pdf'),
    path('visualizar_pdf/<int:id>/', views.visualizar_pdf, name='visualizar_pdf'),
]
