from sanic import Sanic
from sanic import response
from sanic.exceptions import NotFound
from sanic_cors import CORS

app = Sanic(name=__name__)
CORS(app)

# 网页端
@app.route('/')
async def handle_request(request):
    return await response.file("index.html")


# 网页端
@app.route('/base64')
async def handle_request(request):
    return await response.file("base64.html")


@app.route('/result.png')
async def handle_request(request):
    return await response.file("result.png")


# API接口
@app.route('/add', methods=['POST'])
async def handle_test(request):
    json=request.json
    print(json)
    res=None
    if json:
        res='你好~'+json['text']
    
    return response.json({
        'status':200,
        'data': res
        })


if __name__ == '__main__':
    app.error_handler.add(
        NotFound,
        lambda r, e: response.empty(status=404)
    )
    app.run(host='0.0.0.0', port=1234,workers=1)