import RPi.GPIO as GPIO
import servo # servo.py
import rfid  # rfid.py
import ultra # ultra.py
import time
import kamerarevisi as kamera
import requests
import buserled
import multiprocessing
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
ledPinRed=40
ledPinGreen=38

GPIO.setup(ledPinRed, GPIO.OUT)
GPIO.setup(ledPinGreen, GPIO.OUT)

def prosesUtama():
    while True:
        #baca tag rfid
        idRfid, textRfid = rfid.tempel()
        print("id kartu adalah = ", idRfid)
        print("text kartu adalah = ", textRfid)

        # ambil foto
        nomor_pelat = kamera.plate_recognition(idRfid)

        # kirim data
        data = {
        "id_rfid_tag":idRfid,
        "nomor_plat":nomor_pelat
        }
        response = requests.post(
        'http://localhost:5000/apimasuk',
        data=data
        )
        
        responsejson = response.json()
        print(responsejson)

        if responsejson['status'] == 'terdaftar' and 
          responsejson['tempat_parkir'] == 'tersedia':

            GPIO.output(ledPinGreen, True)
            print('masuk atau keluar')
            nomor_pelat = ""

            # buka palang
            servo.bukaServo()

            # periksa keberadaan mobil
            ultra.jarakMobil(15, 400)

            # tutup palang
            time.sleep(1)
            servo.tutupServo()
            GPIO.output(ledPinGreen, False)
                
            GPIO.cleanup()
        elif responsejson['status'] == 'zero' and 
          responsejson['tempat_parkir'] == 'tidak tersedia':

            print('nomor pelat tidak terbaca')
            time.sleep(1)
        elif responsejson['status'] == 'terdaftar' and 
          responsejson['tempat_parkir'] == 'tidak tersedia':
          
            print('id terdaftar dan parkir tidak tersedia')
            time.sleep(1)
        elif responsejson['status'] == 'saldo tidak mencukupi':
            print('saldo tidak mencukupi')
            time.sleep(1)
        else :
            print('id tidak terdaftar')
            time.sleep(1)

def tombolButton():
    while True:
        buserled.tekan()

proses1 = multiprocessing.Process(target=prosesUtama)
proses2 = multiprocessing.Process(target=tombolButton)

if __name__ == '__main__' :
    proses1.start()
    proses2.start()