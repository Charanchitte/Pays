const image= document.getElementsByClassName("button")
const left = document.getElementsByClassName("left");
function myfunction() {
    left[0].style.display = "block";
    image[0].style.display = "none";
}
function myfunct() {
    left[0].style.display = "none";
    image[0].style.display = "inline";
}