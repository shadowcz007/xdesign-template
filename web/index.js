const _WIDHT = 560,
    _HEIGHT = 240;

const mainBoard = document.getElementById('main-board');
const startBtn = document.getElementById('start');
const saveBtn = document.getElementById('save');

class Canvas {
    constructor(element) {
        element.width = window.innerWidth * 0.7;
        element.height = window.innerHeight;
        this.canvas = new fabric.Canvas(element);
        let rect = new fabric.Rect({
            width: _WIDHT,
            height: _HEIGHT,
            left: 0,
            top: 0,
            fill: 'white'
        });

        let group = new fabric.Group([rect], {
            left: 0,
            top: 100,
            angle: 0
        });
        this.canvas.add(group);
        this.canvas.setActiveObject(group);
        let t = this.canvas.getActiveObject();
        t.center(); //全部居中
        t.setCoords();
        this.canvas.discardActiveObject().renderAll();

        this.group = group;

    }
    addImg(imgElement, args = {}, width, height) {
        args = Object.assign(args, {
            left: this.group.get('left') + (args.left || 0),
            top: this.group.get('top') + (args.top || 0),
            originX: 'left',
            originY: 'top'
        })
        var imgInstance = new fabric.Image(imgElement, args);
        imgInstance.scaleToWidth(width);
        imgInstance.scaleToHeight(height);
        this.group.addWithUpdate(imgInstance);
        this.canvas.renderAll();
    }
    addText(text, args = {}) {
        args = Object.assign(args, {
            splitByGrapheme: true,
            left: this.group.get('left') + (args.left || 0),
            top: this.group.get('top') + (args.top || 0),
            originX: 'left',
            originY: 'top',
            // lockScalingX:true,
            // lockScalingY: true,
        });

        if (!args.width) args.width = args.fixedWidth;

        if (args.fixedWidth && args.width && args.width > args.fixedWidth) {
            args.fontSize *= args.fixedWidth / (args.width + 1);
            args.width = args.fixedWidth;
        };

        // console.log(args)
        let t = new fabric.Textbox(text, args);
        this.group.addWithUpdate(t);
        this.canvas.renderAll();
    }
    ungroup() {
        items = this.group._objects;
        items.reverse()
        this.group._restoreObjectsState();
        this.canvas.remove(c.group);
        for (var i = items.length - 1; i >= 0; i--) {
            this.canvas.add(items[i]);
        }
        this.canvas.renderAll();
    }

    // export () {
    //     return this.group.toJSON();
    // }

    download(filename = "demo.png") {
        let base64 = this.group.toDataURL({
            format: 'png',
            multiplier: 2,
        });
        let blob = this.dataURLtoBlob(base64);
        let a = this.createDownloadElement(blob, filename);
        a.click();
    }

    createDownloadElement(blob, filename) {
        let downloadElement = document.createElement('a');
        let href = window.URL.createObjectURL(blob); //创建下载的链接
        downloadElement.href = href;
        downloadElement.download = filename; //下载后文件名
        return downloadElement
    }

    dataURLtoBlob(dataurl) {
        var arr = dataurl.split(','),
            mime = arr[0].match(/:(.*?);/)[1],
            bstr = atob(arr[1]),
            n = bstr.length,
            u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], { type: mime });
    }
}

window.onload = () => {
    window.c = new Canvas(mainBoard);
    let video = document.getElementById('user-camera');
    navigator.mediaDevices
        .getUserMedia({
            video: {
                width: 300,
                height: 300
            },
            audio: false,
        })
        .then((stream) => {
            currentStream = stream;
            video.srcObject = stream;

            video.oncanplay = () => {
                video.height = video.videoHeight;
                video.width = video.videoWidth;
                video.oncanplay = null;
                startBtn.removeAttribute('disabled');
            };
        })
        .catch((error) => {
            console.error(error);
        });
    startBtn.addEventListener('click', async e => {
        e.preventDefault();
        let base64 = getBase64FromVideo(video);
        let res = await postData('/test', {
            base64
        });
        let url = 'data:image/png;base64,' + res.data;


        let img = await createImg(url);

        c.addImg(img, {
            left: 12,
            top: 12
        }, _HEIGHT - 24, _HEIGHT - 24);

        c.addText('TEXT', {
            left: _HEIGHT + 24,
            top: 12,
            fontSize: 32,
            fontWeight: 800,
            width: _WIDHT * 0.8,
            fixedWidth: _WIDHT * 0.8,
        });

        c.addText('2222222TEXT', {
            left: _HEIGHT + 24,
            top: 44,
            fontSize: 23,
            fontWeight: 800,
            // width: _WIDHT * 0.8,
            fixedWidth: 200,
        });

    });


    saveBtn.addEventListener('click', e => {
        e.preventDefault();
        c.download();
    })
};



function getBase64FromVideo(video) {
    let canvas = document.createElement('canvas');
    canvas.width = video.width;
    canvas.height = video.height;
    canvas.getContext('2d').drawImage(video, 0, 0, video.width, video.height);
    let base64 = canvas.toDataURL().replace(/^data:image\/\w+;base64,/, "");
    return base64
}

function createImg(url) {
    return new Promise((resolve, reject) => {
        let img = new Image();
        img.src = url;
        img.onload = () => resolve(img)
    })
}

function postData(url, data) {
    // Default options are marked with *
    return fetch(url, {
            body: JSON.stringify(data), // must match 'Content-Type' header
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, same-origin, *omit
            headers: {
                'user-agent': 'Mozilla/4.0 MDN Example',
                'content-type': 'application/json'
            },
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, cors, *same-origin
            redirect: 'follow', // manual, *follow, error
            referrer: 'no-referrer', // *client, no-referrer
        })
        .then(response => response.json()) // parses response to JSON
}