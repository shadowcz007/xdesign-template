const { spawn } = require('child_process')


function runScript() {
    return spawn('node', [
        "./node_modules/http-server/bin/http-server"
    ]);
};

const subprocess = runScript(); //打印脚本的输出
let isOpen = false;
subprocess.stdout.on('data', (data) => {
    console.log(`data:${data}`);
    setTimeout(() => {
        if (isOpen === false) {
            spawn('open', ['http://127.0.0.1:8081']);
            isOpen = true;
        }
    }, 1500);
});
subprocess.stderr.on('data', (data) => {
    console.log(`error:${data}`);
});
subprocess.stderr.on('close', () => {
    console.log("Closed");
});