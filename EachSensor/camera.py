from picamera import PiCamera
from time import sleep

# Inicializa o objeto PiCamera
camera = PiCamera()

# Ativa a câmera
camera.start_preview()

sleep(5)

# Desativa a câmera
camera.stop_preview()


