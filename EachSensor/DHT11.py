# Carrega as bibliotecas
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

# Define o tipo de sensor
sensor = Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BOARD)

# Define a GPIO conectada ao pino de dados do sensor
pino = 4

# Informações iniciais
print("******************")
print("Lendo os valores de temperatura e umidade")
print("*******************")

while(1):
    # Efetua a leitura do sensor
    umid, temp = Adafruit_DHT.read_retry(sensor, pino)
    
    # Caso leitura esteja ok, mostra os valores na tela
    if umid is not None and temp is not None:
        print("Temperatura = {0:0.1f} Umidade = {1:0.1f}\n".format(temp, umid))
        print("Aguarde 3 segundo para efetuar nova leitura... \n")
        time.sleep(3)
    else:
        # Mensagem de erro de comunicação com o sensor
        print("Falha ao ler dados do DHT11")
