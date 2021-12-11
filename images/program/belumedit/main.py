import RPi.GPIO as GPIO
import servo # servo.py
import rfid  # rfid.py
import ultra # ultra.py
import time
import kamerarevisi as kamera
import requests
GPIO.setwarnings(False)
a = 0
# while a==0:
while True:
    #baca tag rfid
    idRfid, textRfid = rfid.tempel()
    print("id kartu adalah = ", idRfid)
    print("text kartu adalah = ", textRfid)

    # ambil foto
    nomor_pelat = kamera.plate_recognition(idRfid)

    # # ini untuk test test
    # idRfid = 1003735099701
    # nomor_pelat = "dd123xx"

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
    # a = a + 1

    if responsejson['status'] == 'terdaftar' and responsejson['tempat_parkir'] == 'tersedia':
        print('masuk atau keluar')
        nomor_pelat = ""

        # buka palang
        servo.bukaServo()

        # periksa keberadaan mobil
        ultra.jarakMobil(15, 400)

        # tutup palang
        time.sleep(1)
        servo.tutupServo()

        #    if jarakMobil > 6 and jarakMobil < 400:
        #        print('jarak ',jarakMobil, ' cm')
        #        servo.tutupServo()
            
        GPIO.cleanup()
    elif responsejson['status'] == 'zero' and responsejson['tempat_parkir'] == 'tidak tersedia':
        print('nomor pelat tidak terbaca')
    elif responsejson['status'] == 'terdaftar' and responsejson['tempat_parkir'] == 'tidak tersedia':
        print('id terdaftar dan parkir tidak tersedia')
    else :
        print('id tidak terdaftar')