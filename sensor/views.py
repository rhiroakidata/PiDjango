import RPi.GPIO as GPIO
import time, serial, pynmea2, board, busio, sys

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import Adafruit_DHT

import threading, cv2, face_recognition
from .utils import clean
from picamera import PiCamera
from .camera_pi import Camera
from imutils.video import VideoStream
from users.models import User

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

sys.path.append('/home/pi/Desktop/workspace/tests/Pidjango/sensor')


def turnOn(request):
    GPIO.setmode(GPIO.BCM)
    LED_PIN = 26
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, 1)
    time.sleep(5)
    clean()
    return HttpResponse('Led aceso')

def gasSensor(request):
    GPIO.setmode(GPIO.BCM)
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
    GPIO.setmode(GPIO.BCM)
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

def index(request):
    # return the rendered template
    return render(request, "index.html", {})

def generate(cam):

    global outputFrame, lock

    lock = threading.Lock()

    process_this_frame = True

    while True:
        frame = cam.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.125, fy=0.125)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            print(face_locations)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left) in face_locations:
            print(top, right, bottom, left)
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 8
            right *= 8
            bottom *= 8
            left *= 8

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
            if frame is None:
                continue
			# encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

    cam.release()

    cv2.destroyAllWindows()

def camera(request):
    #cam = Camera()
    cam = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    return StreamingHttpResponse(generate(cam), content_type = "multipart/x-mixed-replace; boundary=frame")

# @api_view(['POST'])
# def take_photo(request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     capture_image(user.name, user.cpf)
#     return Response(status=status.HTTP_200_OK)

