import cv2
import numpy as np 
import base64

def resize(image):
    x, y = image.shape[0:2]
    im = cv2.resize(image, (int(y / 2), int(x / 2)))
    return im
    
def cv2_to_base64(image):
    data = cv2.imencode('.png', image)[1]
    return base64.b64encode(data.tostring()).decode('utf8')

def base64_to_cv2(b64str):
    data = base64.b64decode(b64str.encode('utf8'))
    data = np.frombuffer(data, np.uint8)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return data

def gray2rgb(im):
    return cv2.cvtColor(im,cv2.COLOR_GRAY2RGB)

def bgr2gray(im):
    return cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)



from datetime import datetime
import time
# 每n秒执行一次
def timer(n,fun):
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(n)
        if fun!=None:
            fun()

from PIL import Image, ImageGrab

# 读取剪切板图片
def get_clipboard_image():
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        print(im.size, im.mode)

# 5s
timer(1,get_clipboard_image)