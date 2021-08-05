import asyncio
from pyppeteer import launch
import json
from datetime import datetime
import time
# 每n秒执行一次
def timer(n):
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(n)


#发起请求的库
import requests
def download_img(img_url,file_path='test.png'):
#     print (img_url)
    r = requests.get(img_url, stream=True)
#     print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open(file_path, 'wb').write(r.content) # 将内容写入图片
        print("done")
    del r

import numpy as np
from mmcq import get_palette
#提取颜色
def get_colors(url):
    download_img(url,'test.png')
    palettes=[]
    with get_palette('test.png', 8) as palette:
        for p in palette:
            palettes.append([p[0],p[1],p[2]])
    return palettes


#使用scikit learn的余弦相似度计算方法 demo
from sklearn.metrics.pairwise import cosine_similarity

#从target_colors得到与color最近的颜色,用于分类颜色
# rgb空间比hsv来计算更为准确
def get_target_color(color):
    # 颜色分类，简化版
    target_colors=[[244,67,54],[233,30,99],[156,39,176],[103,58,183],[63,81,181],[255,152,0],[139,195,74]]
    sim=cosine_similarity([color]+target_colors)
    index=np.argmax(sim[0][1:-1])
    target=target_colors[index]
    return target

# 可视化结果，用于测试
# tc=get_target_color([222,223,247])
# out = Image.new("RGB", (100, 100), (255, 255, 255))
# d = ImageDraw.Draw(out)
# print(tc)
# d.rectangle(((0, 0), (100, 100)), fill=(tc[0],tc[1],tc[2]))
# out.show()


async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://top.baidu.com/board')
    #页面等待时间,ms, 
    # await page.waitFor(10000)
    await page.screenshot({'path': 'test.jpg'})

    hot_events = await page.evaluate('''
    () => {
        var hots=document.querySelector('.theme-hot');
        var hotTexts=[];

        for(var t of hots.querySelectorAll('.c-single-text-ellipsis')){
            var img = t.parentElement.parentElement.parentElement.querySelector('img');
            //if(!hotTexts.includes(t.innerText)) hotTexts.push(t.innerText);
            if (img) {

             var title = t.parentElement.children[0].innerText,
                 score = t.parentElement.children[1].innerText;

             hotTexts.push({ title: title, score: score, imgurl: img.src });
         }
        };

        return hotTexts

    }
    ''')

    print(hot_events)

    # 用来做图谱可视化
    categories=[[244,67,54],[233,30,99],[156,39,176],[103,58,183],[63,81,181],[255,152,0],[139,195,74]]
    nodes=[]
    links=[]

    # 初始化nodes
    for index in range(len(categories)):
        node={
                "color":categories[index],  
                "id":index,
                "category":index,
                "value":0
            }
        nodes.append(node)

    for x in hot_events:
        #从图片url，提取配色
        x['colors']=get_colors(x['imgurl'])

        for color in x['colors']:
            c=get_target_color(color)
            
            # nodes
            for node in nodes:
                if c==node['color']:
                    node['value']=node['value']+1
            
            # links
            source=None
            target=None
            
            for index in range(len(categories)):
                if c==categories[index]:
                    source=index

            # print('-------',x['colors'])
            for color in x['colors']:
                c=get_target_color(color)
                for index in range(len(categories)):
                    if c==categories[index]:
                        target=index

            print(source,target)
            links.append({
                "source":source,
                "target":target
            })

    graph={
        "categories":categories,
        "nodes":nodes,
        "links":links
        }        

    #列表-->文本
    # hot_events_str='\n'.join(hot_events)
    # hot_events_str=json.dumps(hot_events, indent=4, ensure_ascii=False)
    graph_str=json.dumps(graph, indent=4, ensure_ascii=False)

    # 保存为本地文件
    file = open("graph.json", "w")
    # file = open("hots.txt", "w")
    file.write(graph_str)
    # file.write(hot_events_str)
    # file.write(str(hot_events))
    file.close()

    await browser.close()
    


asyncio.get_event_loop().run_until_complete(main())