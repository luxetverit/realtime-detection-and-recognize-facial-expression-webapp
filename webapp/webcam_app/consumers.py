import cv2
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
import numpy as np
from pathlib import Path
import json
from django.http import StreamingHttpResponse
import base64
from collections import Counter
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from .models import Counseling, DetectedEmotions
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from asgiref.sync import sync_to_async
import os





@database_sync_to_async
def get_counseling_object_or_404(pk):
    return get_object_or_404(Counseling, pk=pk)

@database_sync_to_async
def get_detectdedemotions_object_or_404(pk):
    return get_object_or_404(DetectedEmotions, pk=pk)

@database_sync_to_async
def set_detectdedemotions(detected_emotions,feelcount):
    if feelcount :
        print('onepiece')
        detected_emotions.anger=feelcount['anger']
        detected_emotions.anxiety=feelcount['anxiety']
        detected_emotions.embarrassed=feelcount['embarrassed']
        detected_emotions.hurt=feelcount['hurt']
        detected_emotions.neutral=feelcount['neutral']
        detected_emotions.pleasure=feelcount['pleasure']
        detected_emotions.sad=feelcount['sad']
        detected_emotions.save(update_fields=['anger','anxiety','embarrassed','hurt','neutral','pleasure','sad'])
    else: print('error')
   
        




BASE_DIR = Path(__file__).resolve().parent
CLASSES = ['anger','anxiety','embarrassed','hurt','neutral','pleasure','sad']
# 색상 랜덤하게 뽑아서 적용 다 다르게 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f'{CLASSES[class_id]} ({confidence:.2f})'
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    

# 모델 불러오기 
model = cv2.dnn.readNet(str(BASE_DIR)+"/best.onnx")


def cameracheck(video_capture) :
    if video_capture.isOpened():
        return True
    else: 
        return False


def cam_return():
        video_capture=cv2.VideoCapture(cv2.CAP_ANY,cv2.CAP_DSHOW)
        if cameracheck(video_capture) : #True False
            return video_capture
        else: 
            video_capture=cv2.VideoCapture(cv2.CAP_ANY,cv2.CAP_V4L2)
            return video_capture

feelings=[]
class ImageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pk = self.scope['url_route']['kwargs']['counseling_id']
        self.feelcount=''
        self.counseling = await get_counseling_object_or_404(self.pk)
        self.detected_emotions = await get_detectdedemotions_object_or_404(self.pk)
        await self.accept()

    async def disconnect(self, close_code):
        raise StopConsumer()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if 'image' in data :
            img_data = data['image']
            img_binary = base64.b64decode(img_data.split(',')[1])
            img_buffer = np.frombuffer(img_binary, dtype=np.uint8)
            img = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)
            task= asyncio.create_task(self.stream_video(img))
            await task
        elif data['message'] =='stop' :
            await set_detectdedemotions(self.detected_emotions,self.feelcount)
            await self.close()
            
            

    async def stream_video(self,frame):
        [height, width, _] = frame.shape
        length = max((height, width))
        image = np.zeros((length, length, 3), np.uint8)
        image[0:height, 0:width] = frame
        scale = length / 640
        blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640))
        model.setInput(blob)
        outputs = await asyncio.get_event_loop().run_in_executor(None, model.forward)
        outputs = np.array([cv2.transpose(outputs[0])])
        rows = outputs.shape[1]
        boxes = []
        scores = []
        class_ids = []
    
        for i in range(rows):
            classes_scores = outputs[0][i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            if maxScore >= 0.25:
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                    outputs[0][i][2], outputs[0][i][3]]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

        result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)
        for i in range(len(result_boxes)):
            index = result_boxes[i]
            box = boxes[index]
            detection = {
                'class_id': class_ids[index],
                'class_name': CLASSES[class_ids[index]],
                'confidence': scores[index],
                'box': box,
                'scale': scale}

            draw_bounding_box(frame, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                            round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))

            feelings.append(detection['class_name'])
            
        resized=cv2.resize(frame,dsize=(480, 320),interpolation=cv2.INTER_AREA)
            
        success, image = cv2.imencode('.jpg', resized)
        feelcount=Counter(feelings)
        
        # _, buffer = await asyncio.get_event_loop().run_in_executor(None, cv2.imencode, '.jpg', resized)
        image_bytes = base64.b64encode(image).decode('utf-8')
        send_data = {'image': image_bytes, 'feelings': feelcount}
        
        
        self.feelcount=feelcount
        await self.send(text_data=json.dumps(send_data))
        
        
