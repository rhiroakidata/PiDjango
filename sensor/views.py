import RPi.GPIO as GPIO
import time, serial, pynmea2, board, busio, sys

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import Adafruit_DHT

from picamera import PiCamera

from django.http import HttpResponse

sys.path.append('/home/pi/Desktop/workspace/tests/Pidjango/sensor')
from utils import clean

GPIO.setmode(GPIO.BCM)

def turnOn(request):
    LED_PIN = 26
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, 1)
    time.sleep(5)
    clean()
    return HttpResponse('Led aceso')

def gasSensor(request):
    GPIO.setup(16, GPIO.IN)
    if GPIO.input(16):
        messageGas = 'Ambiente Bom'
        time.sleep(0.2)
    if GPIO.input(16)!=1:
        messageGas = 'Gás detectado'

    clean()

    return HttpResponse(messageGas)

def gpsSensor(request):
    port = "/dev/ttyS0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline().decode("utf-8")

    if newdata[0:6] == "$GPRMC":
        newmsg=pynmea2.parse(newdata)
        lat=newmsg.latitude
        lng=newmsg.longitude
        gps = "Latitude = " + str(lat) + " and Longitude = " + str(lng)
        return HttpResponse(gps)

def dht11Sensor(request):
    sensor = Adafruit_DHT.DHT11

    pino = 4

    umid, temp = Adafruit_DHT.read_retry(sensor, pino)
    
    if umid is not None and temp is not None:
        message = "Temperatura = {0:0.1f} Umidade = {1:0.1f}\n".format(temp, umid)

    else:
        # Mensagem de erro de comunicação com o sensor
        message="Falha ao ler dados do DHT11"

    clean()

    return HttpResponse(message)


def photoSensor(request):
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan = AnalogIn(ads, ADS.P0)

    if chan.value > 15000:
        message = "Ambiente escuro"
        message += "\nValor: {:5d}\tVoltagem: {:5.3f}".format(chan.value, chan.voltage)
        return HttpResponse(message)

    elif chan.value < 15000 and chan.value >= 10000:
        message = "Ambiente pouco iluminado"
        message += "\nValor: {:5d}\tVoltagem: {:5.3f}".format(chan.value, chan.voltage)
        return HttpResponse(message)
 
    else:
        message = "Ambiente muito iluminado"
        message += "\nValor: {:5d}\tVoltagem: {:5.3f}".format(chan.value, chan.voltage)
        return HttpResponse(message)
    
def distanceSensor(request):
    trig = 24
    echo = 23
    sampling_rate = 20.0
    speed_of_sound = 349.10
    max_distance = 4.0
    max_delta_t = max_distance / speed_of_sound

    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    GPIO.output(trig, False)
    time.sleep(1)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    
    while GPIO.input(echo) == 0:
        start_t = time.time()

    while GPIO.input(echo) == 1 and time.time() - start_t < max_delta_t:
        end_t = time.time()

    if end_t - start_t < max_delta_t:
        delta_t = end_t - start_t
        distance = 100*(0.5 * delta_t * speed_of_sound)
    else:
        distance = -1

    message = str(round(distance, 2))

    clean()

    return HttpResponse(message)

def camera(request):
    camera = PiCamera()

    camera.start_preview()

    time.sleep(5)

    camera.stop_preview()



 



