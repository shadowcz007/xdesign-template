function randomSelect(v) {
    var i = Math.round(Math.random() * (v.length - 1));
    return v[i];
}

var input = document.querySelector('input');
var targetId;



new p5();

function setup() {
    createCanvas(500, 300);
    textSize(34);
}

// clear();
function draw() {
    clear();
    background('yellow');
    if (targetId) text(targetId, 10, 50);
}





// console.log(input);
input.addEventListener('change', function(e) {

    var texts = e.target.value;

    targetId = randomSelect(texts.split(' '));
    console.log(targetId);

    // document.querySelector('#result').innerText = id;
})