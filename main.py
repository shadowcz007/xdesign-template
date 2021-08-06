from sanic import Sanic
from sanic import response
from sanic.exceptions import NotFound
from sanic_cors import CORS

import utils

app = Sanic(name=__name__)
CORS(app)


#演示模型的调用
import paddlehub as hub
import cv2
stylepro_artistic = hub.Module(name="stylepro_artistic")



# 网页端
@app.route('/')
def handle_request(request):
    html='<p>Hello world!</p>'
    with open('web/index.html', 'r', encoding='utf-8') as f:
        html=f.read()
    return response.html(html)

# js文件
@app.route("/index.js")
async def get_file(request):
  return await response.file("web/index.js")

# js文件
@app.route("/gif.worker.js")
async def get_file2(request):
  return await response.file("web/gif.worker.js")

# API接口
@app.route('/test', methods=['POST'])
async def handle_test(request):
    # print(request.json)
    json=request.json
    res=None
    if json:
        im=utils.base64_to_cv2(json['base64'])
        
        # im_gray=utils.bgr2gray(im)
        # res=utils.cv2_to_base64(im_gray)

        # 使用算法处理im，返回结果
        result = stylepro_artistic.style_transfer(
            images=[{
                'content': im,
                'styles': [cv2.imread('study/designAI/style.jpeg')]
            }])
        im=result[0]['data']
        res=utils.cv2_to_base64(im)

    return response.json({
        'status':200,
        'data': res
        })



if __name__ == '__main__':
    app.error_handler.add(
        NotFound,
        lambda r, e: response.empty(status=404)
    )
    app.run(host='0.0.0.0', port=8888,workers=1)