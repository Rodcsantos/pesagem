import socket
import re
from decimal import Decimal
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import RegistroPesagem
from .forms import RegistroPesagemForm
import cv2
import base64
import os
from django.conf import settings

# Diretório temporário para imagenss
TEMP_IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, 'temp_images')
os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)


def captura_peso():
    IP_BALANCA = '192.168.2.48'  # Substitua pelo IP correto da balança
    PORTA_BALANCA = 9000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # Timeout de 5 segundos

    try:
        sock.connect((IP_BALANCA, PORTA_BALANCA))
        dados = sock.recv(1024)
        mensagem = dados.decode('utf-8', errors='ignore').strip()

        # Captura os números antes do "kg"
        peso_match = re.search(r'\d+', mensagem)
        if peso_match:
            peso_str = peso_match.group().lstrip('0')  # Remove zeros à esquerda
            peso_num = int(peso_str) if peso_str else 0
            return Decimal(peso_num / 1000000)  # Converte para kg, se necessário

    except Exception as e:
        print(f"Erro ao capturar o peso: {e}")
    finally:
        sock.close()
    return None


def captura_imagem(camera):
    """Captura imagem da câmera e retorna em formato base64"""
    try:
        success, frame = camera.read()
        if not success or frame is None:
            return None

        img_encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        if not img_encoded[1].any():
            return None

        img_base64 = base64.b64encode(img_encoded[1].tobytes()).decode('utf-8')
        return img_base64
    except Exception as e:
        print(f"Erro ao capturar imagem: {e}")
        return None
    finally:
        camera.release()


def registrar_pesagem(request):
    peso = captura_peso()  # Captura o peso automaticamente da balança

    if request.method == 'POST':
        form = RegistroPesagemForm(request.POST, request.FILES)
        if form.is_valid():
            registro = form.save(commit=False)

            # Verifica se o peso de entrada foi alterado manualmente
            peso_entrada_manual = request.POST.get('peso_entrada')
            if peso_entrada_manual:
                try:
                    registro.peso_entrada = Decimal(peso_entrada_manual)  # Usa o peso manual
                except Exception as e:
                    messages.error(request, f"Erro ao converter o peso de entrada: {e}")
                    return redirect('pesagem:registrar_pesagem')
            elif peso is not None:  # Se não foi informado manualmente, usa o peso da balança
                registro.peso_entrada = peso
            else:
                messages.error(request, "Peso de entrada não capturado nem informado.")
                return redirect('pesagem:registrar_pesagem')

            # Registra apenas a data de entrada
            registro.data_entrada = timezone.now()

            # Captura a imagem de entrada
            camera = cv2.VideoCapture("rtsp://admin:Usuario@2024@192.168.100.50:554/Streaming/Channels/101/")
            imagem_entrada = captura_imagem(camera)
            if imagem_entrada:
                registro.imagem_entrada = imagem_entrada  # Salva a imagem em base64
            elif 'imagem_entrada_upload' in request.FILES:
                registro.imagem_entrada_upload = request.FILES['imagem_entrada_upload']  # Salva imagem via upload

            # Remove a lógica automática de preenchimento de peso_saida
            # A lógica de saída será tratada na função específica para saída

            # Salva o registro da pesagem
            registro.save()
            messages.success(request, "Pesagem registrada com sucesso.")
            return redirect('pesagem:listar_pesagens_pendentes')




        else:
            messages.error(request, "Erro ao registrar a pesagem. Verifique os dados.")
    else:
        form = RegistroPesagemForm(initial={'peso_entrada': peso})  # Preenche o peso de entrada com o peso atual

    return render(request, 'pesagem/registrar_pesagem.html', {'form': form, 'peso': peso})



def registrar_peso_saida(request, id):
    registro = get_object_or_404(RegistroPesagem, id=id)
    
    if registro.peso_entrada is None:
        return redirect('pesagem:pesagem_pendente')

    if request.method == 'POST':
        peso_saida = request.POST.get('peso_saida')

        # Captura o peso da balança automaticamente se o campo estiver vazio
        if not peso_saida:
            peso_saida = captura_peso()  # Função que retorna o peso atual

        if peso_saida:
            registro.peso_saida = float(peso_saida)
            registro.data_saida = timezone.now()

            # Captura e salva a imagem de saída
            imagem_saida_base64 = captura_imagem(cv2.VideoCapture("rtsp://admin:Usuario@2024@192.168.100.50:554/Streaming/Channels/101/"))
            if imagem_saida_base64:
                # Salva imagem em base64 (caso contrário você pode querer gravar como arquivo)
                registro.imagem_saida = imagem_saida_base64  # Salva imagem em base64
            elif 'imagem_saida' in request.FILES:
                imagem_saida_file = request.FILES['imagem_saida']
                # Salva a imagem via upload
                registro.imagem_saida_upload.save(f"saida_{registro.id}.jpg", imagem_saida_file)

            # Salva o registro
            registro.save()
            return redirect('pesagem:listar_pesagens_pendentes')




    return render(request, 'pesagem/registrar_peso_saida.html', {'registro': registro, 'peso_atual': captura_peso()})




def listar_pesagens_pendentes(request):
    registros_pendentes = RegistroPesagem.objects.filter(peso_entrada__isnull=False, peso_saida__isnull=True  ).order_by('-data_entrada')
    return render(request, 'pesagem/listar_pesagens_pendentes.html', {'registros_pendentes': registros_pendentes})


def listar_pesagens_realizadas(request):
    registros_realizados = RegistroPesagem.objects.filter(peso_saida__isnull=False)
    return render(request, 'pesagem/listar_pesagens_realizadas.html', {'registros_realizados': registros_realizados})

def pesagem_sucesso(request):
    return render(request, 'pesagem/sucesso.html')

def gerar_pdf(request, id):
    registro = get_object_or_404(RegistroPesagem, id=id)

    # Preparando os dados para o template
    data_entrada_formatada = registro.data_entrada.strftime('%d/%m/%Y %H:%M') if registro.data_entrada else 'Não disponível'
    data_saida_formatada = registro.data_saida.strftime('%d/%m/%Y %H:%M') if registro.data_saida else 'Não disponível'
    peso_dif = (registro.peso_entrada or 0) - (registro.peso_saida or 0)
    peso_dif2 = round((registro.peso_entrada) - (registro.peso_saida ))



    
    context = {
        'registro': registro,
        'data_entrada_formatada': data_entrada_formatada,
        'data_saida_formatada': data_saida_formatada,
        'peso_dif': peso_dif,
        'peso_dif2': peso_dif2
    }

    # Renderizando o template HTML
    html_string = render_to_string('pesagem/pdf_template.html', context)

    # Gerando o PDF a partir do HTML renderizado
    pdf = HTML(string=html_string).write_pdf()

    # Criando a resposta HTTP com o conteúdo PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pesagem_{registro.id}.pdf"'

    return response

def visualizar_pdf(request, id):
    # Recupera o registro da pesagem
    registro = get_object_or_404(RegistroPesagem, id=id)
    
    # Dados para o contexto do template
    context = {
        'registro': registro
    }

    # Renderiza o template em HTML
    html_string = render_to_string('pesagem/pdf_template.html', context)
    
    # Passa o HTML para o template de visualização
    return render(request, 'pesagem/visualizar_pdf.html', {'html_string': html_string})