function setName(){
    var sex = document.getElementById('sexuality').value;
    document.querySelector('#MomName').textContent = sex;
}

window.onload = function (){
    document.getElementById('userErstellen').onclick = setName;
}