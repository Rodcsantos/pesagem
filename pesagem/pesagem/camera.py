import cv2
from django.http import StreamingHttpResponse

def gen(camera):
    while True:
        # Capture frame a partir do feed RTSP
        success, frame = camera.read()
        if not success:
            break

        # Codifica o frame como JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            break

        # Retorna o frame codificado no formato MJPEG
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

def video_feed(request):
    # Conectar ao feed RTSP da câmera
    camera = cv2.VideoCapture("rtsp://admin:Usuario@2024@192.168.100.50:554/Streaming/Channels/101/")
    return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')
