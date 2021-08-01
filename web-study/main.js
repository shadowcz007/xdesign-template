function randomSelect(v) {
    var i = Math.round(Math.random() * (v.length - 1));
    return v[i];
}

var input = document.querySelector('input');

console.log(input);
input.addEventListener('change', function(e) {

    var text = e.target.value;

    var id = randomSelect(text.split(' '));
    console.log(id);

    document.querySelector('#result').innerText = id;
})