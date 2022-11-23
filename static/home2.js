function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav_left") {
        x.className += " responsive";
    } else {
        x.className = "topnav_left";
    }
}
function myFunction() {
    var x = document.getElementById("myTopnav2");
    if (x.className === "topnav_right") {
        x.className += " responsive";
    } else {
        x.className = "topnav_right";
    }
}
window.addEventListener('scroll', function () {
    let header = document.getElementById("myTopnav");
    let windowPosition = window.scrollY > 0;
    header.classList.toggle('scrolling-active', windowPosition);
})