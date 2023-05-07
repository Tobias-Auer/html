function add() {
    let a=4;
    let b=5;

    console.log("Commited!!");
    let c = a + b;
    var element = document.getElementById("meinName");
    element.innerText = c;
}

function readInput() {
    let element = document.getElementById("meinName");
    let input = document.getElementById("name").value
    element.innerText = input
}