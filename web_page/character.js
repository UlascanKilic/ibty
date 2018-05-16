function Character(id, skin, posX, posY, nick) {
  this.totalAnimation = 3;
  this.animState = 0;
  this.moveState = false;
  this.direction = "S";
  this.skin = skin;
  this.offsetX = json.characters[this.skin].offsetX;
  this.offsetY = json.characters[this.skin].offsetY;
  this.nick = nick;

  RoomContent.call(this, id, skin + this.direction + this.animState, posX, posY, "character", nick);

  this.setDirection = function (directionName) {
    this.direction = directionName;
    this.textureName = this.skin + this.direction + this.animState;
    this.updateTextureSourceElement();
  };

  this.updateTextureSourceElement();

  this.onclick = function () {
   
    socket.emit("click", {"id":this.id, "type":"character"});
  };

  var walkX, walkY, walkTime;
  var walkingState = false;
  var isPlayerRightOnWalkX = false;
  var isPlayerUpperOnWalkY = false;
  var animStateSayac = 3;
  var animTimeSayac = 0;
  var w = $("#game").innerWidth;
  var h = $("#game").innerHeight;
  this.updateAnim = function (direct, deltaTime) {
    this.setDirection(direct);
    var skinStates = [1, 0, 2, 0];
    this.animState = skinStates[animStateSayac % 4];
    animTimeSayac += deltaTime;


    var walkDiffX = walkX - this.positionX;
    var walkDiffY = this.positionY - walkY;
    var walkDistanceX = walkDiffX / (walkTime / deltaTime) || 0;
    var walkDistanceY = walkDiffY / (walkTime / deltaTime) || 0;
    var deltayol = Math.sqrt((walkDistanceX * walkDistanceX) + (walkDistanceY * walkDistanceY))

    if (animTimeSayac >= (3 / deltayol || 1)) {
      animTimeSayac = 0;
      animStateSayac++;
    }
  };



  this.UpdateBubble = function () {
    var bubbleH = $("#toolTip_" + this.id).height();
    var tailH = $("#toolTip_" + this.id + " > #tail2").height();

    $("#toolTip_" + this.id).css("left", (((this.positionX + 0.5) * (gameW / 13)) - 15) + "px");
    $("#toolTip_" + this.id).css("top", (((this.positionY - 0.5) * (gameH / 9)) - (bubbleH + tailH)) + "px");
  }

  this.updateNick = function () {
    var nickH = $("#nick_" + this.id).height();
  
    $("#nick_" + this.id).css("left", (((this.positionX + 0.5) * (gameW / 13)) - (($("#nick_" + this.id).width() / 2))) + "px");
    $("#nick_" + this.id).css("top", (((this.positionY - 0.5) * (gameH / 9)) - nickH) + "px");
  }

  this.speech = function (text) {
    var speechText = text;
    var toolTipID = "toolTip_" + this.id;
    var messageID = "message_" + this.id;
    if ($("#" + toolTipID).length <= 0) {

      var toolTip = document.createElement('div');
      toolTip.id = toolTipID;
      toolTip.className = "toolTip";
      document.getElementsByTagName('body')[0].appendChild(toolTip);

      var message = document.createElement('p');
      message.id = messageID;
      message.className = "message";
      message.innerHTML = "<span class='span_nick'>" + this.nick + " : </span> <span class='span_message'>Message</span>";
      toolTip.appendChild(message);

      if (this.constructor.name == "NPC") {
       
        $("#toolTip_" + this.id + " .span_nick")[0].style.color = "blue";
       

      }

      var tail1 = document.createElement('div');
      tail1.id = "tail1";
      toolTip.appendChild(tail1);

      var tail2 = document.createElement('div');
      tail2.id = "tail2";
      toolTip.appendChild(tail2);
    }
    this.UpdateBubble();

    if ($("#" + toolTipID).is(":visible")) {
      return true;
    }
    else {
      $("#" + toolTipID).fadeIn(1000);
      var character = this;
      let strLen = speechText.length;
      let text = speechText;
      let to = strLen,
        from = 0;

      animate({
        duration: 1000,
        timing: quad,
        draw: function (progress) {
          let result = (to - from) * progress + from;
          $("#" + messageID + "> .span_message").text(text.substr(0, Math.ceil(result)));
          character.UpdateBubble();
        }
      });

      //   $("#backP").append("Player : "+text + "</br>");
    }
    setTimeout(
      function () {
        $("#" + toolTipID).fadeOut(500);
      }, 5000);

    function quad(timeFraction) {
      return Math.pow(timeFraction, 2)

    }
    //    $("#message").text($("#textArea").val());
    //    $("#toolTip").fadeToggle(1000);    
  }


  
  this.moveTo = function (x, y, time) {
    walkX = x;
    walkY = y;
    walkTime = time;
    walkingState = true;

    if (this.positionX > x) {
      isPlayerRightOnWalkX = true;
    }
    else {
      isPlayerRightOnWalkX = false;
    }
    if (this.positionY > y) {
      isPlayerUpperOnWalkY = true;
    }
    else {
      isPlayerUpperOnWalkY = false;
    }
  }

  this.update = function (deltaTime) {


    if (walkingState) {
      var walkDiffX = walkX - this.positionX;
      var walkDiffY = this.positionY - walkY;

      var walkDistanceX = walkDiffX / (walkTime / deltaTime) || 0;
      var walkDistanceY = walkDiffY / (walkTime / deltaTime) || 0;

      this.positionX += walkDistanceX;
      this.positionY -= walkDistanceY;
      walkTime -= deltaTime;
      //    $("#toolTip").css("left", $('#cnvs_roomContens').width()-($('#cnvs_roomContens').width()/this.positionX)+"px");
      //    $("#toolTip").css("top", $('#cnvs_roomContens').height()-(($('#cnvs_roomContens').height()/this.positionY)+1)+"px");

      this.UpdateBubble();

      if (isPlayerRightOnWalkX) { // WEST
        if (this.positionX < walkX) {
          this.positionX = walkX;
          this.positionY = walkY;
          walkingState = false;
          this.animState = 0;
        }
      }
      else {// EAST  
        if (this.positionX > walkX) {
          this.positionX = walkX;
          this.positionY = walkY;
          walkingState = false;
          this.animState = 0;
        }
      }
      if (isPlayerUpperOnWalkY) {// SOUTH         
        if (this.positionY < walkY) {
          this.positionY = walkY;
          this.positionX = walkX;
          walkingState = false;
          this.animState = 0;
        }
      }
      else {// NORTH   
        if (this.positionY > walkY) {
          this.positionX = walkX;
          this.positionY = walkY;
          walkingState = false;
          this.animState = 0;
        }
      }
      if (this.positionY == walkY && this.positionX == walkX) {
        walkingState = false;
        this.animState = 0;
      }

      if (Math.abs(walkDiffX) > Math.abs(walkDiffY)) {
        //X
        if (walkDiffX > 0) {
          //E
          this.updateAnim("E", deltaTime);
        }
        else {
          //W
          this.updateAnim("W", deltaTime);
        }
      }
      else {
        //Y
        if (walkDiffY > 0) {
          //N
          this.updateAnim("N", deltaTime);
        }
        else {
          //S
          this.updateAnim("S", deltaTime);
        }
      }
    }
    this.updateNick();

  };
}

