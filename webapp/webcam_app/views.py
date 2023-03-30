from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import cv2
import numpy as np
from django.views.decorators import gzip
from pathlib import Path


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
# model = cv2.dnn.readNet('best.onnx')
model = cv2.dnn.readNet(str(BASE_DIR)+"/best.onnx")
# 비디오 캡처 파트
@gzip.gzip_page
def webcam_feed(request):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Failed to open video file')
        exit()

    # 비디오의 각 속성 받기 
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # mp4 output 파일 내보내기 => 파일명 변경 고객명 날짜 받아서 변수로 취급후 변경
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 30, (frame_width, frame_height))

    # 화면 프레임단위로 움직임
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
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
            
            #박스 작업 
            draw_bounding_box(frame, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                            round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))

        # output 저장
        out.write(frame)
        
        # 비디오 실행
        cv2.imshow('Frame', frame)
        
        # 300ms 대기 
        key = cv2.waitKey(300)
        
        # 테스트용 q아웃 
        if key == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    # return HttpResponse('')
    return render(request, 'webcam/close.html')
    



# @csrf_exempt
# def process_frame(request):
#     logs = []
#     if request.method == 'POST':
#         try:
#             logs.append({'method': request.method, 'path': request.path, 'data': request.POST.dict()})
#             print(logs)
#
#             print(request.FILES)
#             print(request.POST)
#
#             frame = request.FILES['frame'].read()
#             # process the frame as needed
#             return HttpResponse(status=204)
#         except KeyError:
#             return HttpResponseBadRequest('Missing frame field')


def socket(request):
    return render(request, 'webcam/socket.html')