window.addEventListener('DOMContentLoaded', () => {
  var oldScrollY = 0;
var div = document.getElementById("fixedDiv");

window.onscroll = function() {
  var scrolled = window.pageYOffset || document.documentElement.scrollTop;
  var dY = scrolled - oldScrollY;
  
  if ( dY > 0 ){
    div.className = "fixed fixed-bottom";
  } else {
    div.className = "fixed fixed-top";
  }
  
  oldScrollY = scrolled;
}


})