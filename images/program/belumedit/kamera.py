import picamera
import time
import requests

def plate_recognition(rfid_tag) :
    # img_name = f"/static/imgpelat/{rfid_tag}.jpg"
    img_name = f"{rfid_tag}.jpg"

    camera = picamera.PiCamera()

    looping = True
    
    while looping:
        camera.start_preview()
        time.sleep(1)
    
        #print("sedang mengambil gambar")
        camera.capture(img_name)
        #print("gambar diambil")

        camera.stop_preview()

        api_token = '6955f6366338a6078826f7d89031c17179986082'

        with open(img_name, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                files=dict(upload=fp),
                headers={'Authorization': 'Token ' + api_token})
        result = response.json()
        
        try :
            plate = result.get("results")[0].get("plate")
            looping = False
        except IndexError :
            #print("mengambil gambar lagi")
            print('nomor plat tidak terbaca')
            plate = "zero"
            looping = False

    camera.close()
    print(plate.upper())
    return plate.upper()