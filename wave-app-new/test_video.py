### STORE THE VIDEOS IN q.app.stored_video

import cv2
from model.model_interface import ModelInference
import time

FPS = 1/30
FPS_MS = int(FPS * 1000)

model = ModelInference('ultralytics/yolov5', 'model/model_artifacts.pt')

# load video from app
vidcap = cv2.VideoCapture('fire_video_1.mp4')
vidcap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

success, image = vidcap.read()
prediction = model.inference(image)
count = 0
pred = 0

while success:

    if count % 30 == 0:
        prediction = model.inference(image)
        image = model.create_image(image, prediction)
        pred += 1
        print('30 ELAPSED')

    time.sleep(FPS)
    success, image = vidcap.read()
    count += 1

print('Counted', count)
print('Predicted', pred)