from enum import Enum
class SelState(Enum):
    NONE = 0 #초기 상태
    CUT = 1 #잘라내기
    BLUR = 2 #블러링
    SHARP = 3 #샤프닝
    MOSAIC = 4 #모자이크
    
    LBUTTON_DOWN = 10 #마우스 클릭 상태
    LBUTTON_UP = 11 #마우스 클릭에서 뗀 상태
