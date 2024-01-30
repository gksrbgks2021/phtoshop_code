# About The Project
---
### PyQt5 , Open-CV 를 사용한 포토샵 앱

### UI 구상도

<img src='https://github.com/gksrbgks2021/phtoshop_code/assets/39733405/da34e50f-9964-4d7b-b756-2b6aad0339a6' width='60%'/>

### 기능 나열
- 배열 연산 이용한 회전 , 좌우반전
- 마우스 오버레이 시 UI 움직이는 기능
- RGB 트랙바
- 반전 필터
- salt and peper 기법을 사용한 점묘법 필터
- 이미지 자르기, 샤프닝, 블러링 기능

### 핵심 기능
- 점묘법 필터 1, 2 를 직접 구현하였음. 각각 밝은색, 어두운색으로 구별 가능
- 이미지에 검은색, 또는 밝은색 점을 랜덤 좌표에 할당. 그후 erode, dilate 메소드로 마치 점으로 그림을 그린것 같은 필터 효과를 구성하였음.

<img src='https://github.com/gksrbgks2021/phtoshop_code/assets/39733405/ccb3eb94-95c3-4645-9b6a-97b3ad62c735' width='40%'/>

```python
#노이즈 뿌리는 함수
    def add_noise(self,img, noise_pixel):
        global weight
        print(noise_pixel)
        b,g,r = cv2.split(img)#rgb 분리
        rgb_list = [b,g,r]

        # img의 행 열을 가져온다.
        row , col = rgb_list[0].shape
        weight = int(math.sqrt(row * col // 40000)) #크기에 따른 노이즈 크기 조절
        if weight < 1 : weight =1
        # 노이즈 개수 지정
        number_of_pixels = 10000*weight
        #print(weight)
        for j in range(number_of_pixels):
            #랜덤 좌표에다 노이즈 부여
            y=random.randint(0, row - 1-weight)
            x=random.randint(0, col - 1-weight)
            
            for i in range(3):#rgb 위치는 동일
                div_img = rgb_list[i] #rgb 리스트 하나 불러온 다음  
                #div_img[y:y+2][x:x+2] = 255 #(255,255,255) 가중치 네모 사이즈 만큼 흰색 노이즈 뿌린다.
                for a in range(weight):
                    for b in range(weight):
                        div_img[y+a][x+b] = noise_pixel
        
        img = cv2.merge(rgb_list) #rgb 합침
        return img
    
    #점묘법 필터 함수
    def pointillism_filter(self,img):
        img_noise = self.add_noise(img.copy(),255)
        kernel = np.ones((3*weight+1,3*weight+1), np.uint8) / ((3*weight+1) * (3*weight+1) ) # 가중치에 따른 마스크 생성
        img_noise = cv2.erode(img_noise,kernel) #erode 연산으로 화이트 노이즈 없엠.
        return img_noise

    #밝은 점묘법 필터 함수
    def pointillism_filter2(self,img):
        img_noise = self.add_noise(img.copy(),0)# (0,0,0) 노이즈를 뿌린다.
        kernel = np.ones((3*weight+1,3*weight+1), np.uint8) / 9 # 가중치에 따른 마스크 생성
        img_noise = cv2.dilate(img_noise,kernel) #dilate 연산으로 객체 팽창.
        return img_noise

    def get_rgb(self):
        return self.rgb

```


### 시연 영상 클릭
[![비디오링크](https://img.youtube.com/vi/PwDfYspcBI8/0.jpg)](https://www.youtube.com/watch?v=PwDfYspcBI8)
