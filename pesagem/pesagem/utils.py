import cv2
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

def captura_imagem_rtsp(camera):
    try:
        # Captura um frame do feed RTSP
        success, frame = camera.read()
        if not success:
            return None  # Se falhar, retorna None

        # Usar a biblioteca Pillow para manipular a imagem
        imagem_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        imagem = Image.open(BytesIO(imagem_bytes))

        # Converte a imagem para um formato compatível para o Django (ex: PNG)
        imagem.save(imagem_bytes, format='PNG')
        imagem_bytes.seek(0)

        return ContentFile(imagem_bytes.read(), 'imagem.png')

    except Exception as e:
        print(f"Erro ao capturar imagem do RTSP: {e}")
        return None
