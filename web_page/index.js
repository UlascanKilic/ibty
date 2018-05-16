var Groom;
var gameW = 0;
var gameH = 0;
var BubbleH = 0;
var nick = "";
var skin = "";
var mapImage = "";

if (location.search.indexOf('refresh=') >= 0) {
  var loc = "index.html"; // or a new URL
  window.location.href = loc; // random number

}

ReadCharactersJson();
ReadEntitiesJson();
ReadRoomsJson();

var setMapImage = function (mapImageText) {
 // mapImage = mapImageText;
 console.log('#texture_rooms_'+mapImageText);

  var canvasOyunEkrani = document.getElementById("cnvs_oyunEkrani");
  var ctxOyunEkrani = canvasOyunEkrani.getContext("2d");
  ctxOyunEkrani.clearRect(0, 0, canvasOyunEkrani.width, canvasOyunEkrani.height);
  ctxOyunEkrani.drawImage($('#texture_rooms_'+mapImageText)[0], 0, 0, 416, 288);
};
function StartRendering(room) {
  var maxFPS = 60;

  function animate() {
    setTimeout(function () {
      requestAnimationFrame(animate);
      room.render();
    }, 1000 / maxFPS);
  }
  animate();
}
function ResizeGameWH() {
  var windowWidth = window.innerWidth;
  var windowHeight = window.innerHeight;
  if (windowHeight >= ((windowWidth / 13) * 9)) {
    gameW = windowWidth;
    gameH = ((windowWidth / 13) * 9);
    // $(".game").style.width = gameWidth+"px";
  }
  else if (windowWidth >= ((windowHeight / 9) * 13)) {
    gameW = (windowHeight / 9) * 13;
    gameH = windowHeight;
    //  $(".game").style.height = gameHeight+"px";
  }

  var oran = 1;
  var chatWidth = 260;
  if (windowWidth - gameW < chatWidth) {
    var IhtiyacPix = (chatWidth - (windowWidth - gameW));
    oran = (1 / (gameW / (gameW - IhtiyacPix)));
  }

  gameW *= oran;
  gameH *= oran;
  $(".game").css("width", gameW);
  $(".game").css("height", gameH);
  $(".hd-option-window").css("height", gameH);
}



window.onresize = function (event) {
  ResizeGameWH();
};
window.addEventListener("load", function () {
  // $(".hd-option-window").removeAttr("style").hide();
  var load_screen = document.getElementById("load_screen");
  document.body.removeChild(load_screen);


});

window.onload = function () {

  muzik = document.getElementById("muzik");
  muzik.pause();
  ResizeGameWH();

  var canvasWater = document.getElementById("cnvs_suAlani");
  var ctxWater = canvasWater.getContext("2d");
  var img = document.getElementById("texture_entity_su1_5");
  ctxWater.drawImage(img, 0, 0, 416, 288);
  var sayac = 1;
  setInterval(function () {
    var img = document.getElementById("texture_entity_su" + sayac + "_5");
    ctxWater.drawImage(img, 0, 0, 416, 288);
    if (sayac < 12) {
      sayac++;
    }
    else {
      sayac = 1;
    }
  }, 1800);

  var canvasRoomContent = document.getElementById("cnvs_roomContens");
  var ctxRoomContent = canvasRoomContent.getContext("2d");

  ctxRoomContent.imageSmoothingEnabled = false;

  var room = new Room(ctxRoomContent, canvasRoomContent);

  room.render();
  StartRendering(room);
  Groom = room;

  $('.game').click(function (e) {
    var elm = $(this);
    var xPos = (e.pageX - elm.offset().left) / $('#cnvs_roomContens').width();
    var yPos = (e.pageY - elm.offset().top) / $('#cnvs_roomContens').height();

    var clickedX = xPos * 13;
    var clickedY = yPos * 9;
    room.click(clickedX, clickedY);
    // Groom.getRoomContent("p1").moveTo((xPos * 13) - 0.5, (yPos * 9) - 0.5, 1000);
  });
}
