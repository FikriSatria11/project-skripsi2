import picamera
import time
import requests

def plate_recognition(rfid_tag) :
    img_name = f"{rfid_tag}.jpg"

    camera = picamera.PiCamera()

    looping = True
    
    while looping:
        camera.start_preview()
        time.sleep(1)
    
        camera.capture(img_name)

        camera.stop_preview()

        api_token = 'b79c79cca32e8f0eb065992e883a9ece23143829'

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
            print('nomor plat tidak terbaca')
            plate = "zero"
            looping = False

    camera.close()
    print(plate.upper())
    return plate.upper()