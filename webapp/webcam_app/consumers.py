import cv2
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
import numpy as np
from pathlib import Path
import json
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import base64
from collections import Counter
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer

BASE_DIR = Path(__file__).resolve().parent
CLASSES = ['anger','anxiety','embarrassed','hurt','neutral','pleasure','sad']

colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))


# 색상 랜덤하게 뽑아서 적용 다 다르게 
def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f'{CLASSES[class_id]} ({confidence:.2f})'
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    

# 모델 불러오기 
model = cv2.dnn.readNet(str(BASE_DIR)+"/best.onnx")


# class chatCosnumer(WebsocketConsumer) :
#     def connect(self):
#         self.accept()
        
        
#         self.send(text_data=json.dumps({
#             'type':'connection_established',
#             'message':'you are now connected'
#         }))
        
#     def receive(self, text_data, bytes_data=None):
#         text_data_json=json.loads(text_data)
#         message=text_data_json['message']
        
        
    
    
    
#     def disconnect(self, code):
#         return super().disconnect(code)
    




cap= cv2.VideoCapture(cv2.CAP_DSHOW+0)

class VideoConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        # 연결만 해줍니다. 그 이후에는 프론트단에서 동작이 있으면 receive 함수로 연결이 되게 됩니다.
        await self.accept()




    async def disconnect(self, close_code):
        self.cap.release()
        raise StopConsumer




    async def receive(self, text_data):
        data=json.loads(text_data)
        
        if data['type']=="control" and data['message']=="close":
            self.disconnect()
            
        if data['type']=="control" and data['message']=="start":
             
            # 비디오의 각 속성 받기 
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)

            # mp4 output 파일 내보내기 => 파일명 변경 고객명 날짜 받아서 변수로 취급후 변경
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height))
            
            all_feeling=[]
            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                # Perform any OpenCV operations on the frame here
                # 화면 길이 input 640에 맞게 변경     
                [height, width, _] = frame.shape
                length = max((height, width))
                image = np.zeros((length, length, 3), np.uint8)
                image[0:height, 0:width] = frame
                scale = length / 640
                
            #  Yolov8 모델은 전치해줘야 하나봄 
                blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640))
                model.setInput(blob)
                outputs = model.forward()
                outputs = np.array([cv2.transpose(outputs[0])])
                rows = outputs.shape[1]
                
                boxes = []
                scores = []
                class_ids = []
                    
            # 한장의 사진에 각 x,y, confidence 받음 

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
                
                detections = []
                for i in range(len(result_boxes)):
                    index = result_boxes[i]
                    box = boxes[index]
                    detection = {
                        'class_id': class_ids[index],
                        'class_name': CLASSES[class_ids[index]],
                        'confidence': scores[index],
                        'box': box,
                        'scale': scale}
                    # ditections 내부에 dections 정보 다 포함되어 있음
                    
                    detections.append(detection)
                    all_feeling.append(detection['class_name'])
                    #박스 작업 
                    draw_bounding_box(frame, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                                    round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))

                    # output 저장
                    out.write(frame)

                    # Encode the frame as a JPEG image
                    success, image = cv2.imencode('.jpg', frame)
                    img_bytes = image.tobytes()

                    if not success:
                        break
                    
                    img_base64 = base64.b64encode(img_bytes)
                    
                    # Send the processed image back to the client


                    await self.send(json.dumps({
                        "image":img_base64.decode("utf-8"),
                        
                        
                        
                    }))
                    
                    # print(detections)
                    await asyncio.sleep(0.05)
                feeling_counter=Counter(all_feeling)
                # await self.send(json.dumps({
                #     "feelings": feeling_counter
                # }))
      