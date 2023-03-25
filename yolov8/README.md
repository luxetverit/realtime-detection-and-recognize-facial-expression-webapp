# YOLOv8 Large model based

# v8 nano vs v8 large 

## 쟁점
- F1 Confidence Curve나  PR 커브를 보면 불안 당황 같은 경우에 많이 아래로 치우쳐 있거나 기울기가 완만하지 않음
- 그럼에도 불구하고 map가 좋게 나오는 이유는 기쁨, 중립, 분노가 평균 수치를 많이 높여줬기 때문

- large 모델 같은 경우에는 그나마 f1커브에서 nano 모델보다 간격이 줄어있는 편이다 


# v5 nano 모델

- v8 nano 모델과 비교하여 확연한 차이가 나지만 v5가 다른 pt이외의 모델에서도 많이 사용되고 있으며 
- 상대적으로 빠르다고 한다 만약 정말 빠르게 처리해야 한다면 v5nano > v8 nano 후 이외의 순서일것 같다