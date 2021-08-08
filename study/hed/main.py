import cv2
import numpy as np
import matplotlib.pyplot as plt

# 加载模型
# hed_pretrained_bsds.caffemodel预训练模型下载http://vcl.ucsd.edu/hed/hed_pretrained_bsds.caffemodel
# deploy.prototxt 下载https://github.com/s9xie/hed/tree/master/examples/hed
net = cv2.dnn.readNet('model/deploy.prototxt', 'model/hed_pretrained_bsds.caffemodel')

#Resize input image to a specific width and height 
width=400
height=400

img = cv2.imread('test2.png')  

inp = cv2.dnn.blobFromImage(img, scalefactor=1.0, size=(width,height),
                               mean=(104.00698793, 116.66876762, 122.67891434),
                               swapRB=False, crop=False)
net.setInput(inp)
 
out = net.forward()

out = out[0, 0]
out = cv2.resize(out, (img.shape[1], img.shape[0]))
out=cv2.cvtColor(out,cv2.COLOR_GRAY2RGB) 

out=1-out

plt.imshow(out)
plt.show()

#二值化
# t=cv2.cvtColor(np.uint8(out*255),cv2.COLOR_RGB2GRAY)
# thresh_map = cv2.threshold(t, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# plt.imshow(cv2.cvtColor(thresh_map,cv2.COLOR_GRAY2RGB))
# plt.show()