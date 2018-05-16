var pixelSize = 32;

function Room(ctx, canvas) {
  this.ctx = ctx;
  this.canvas = canvas;
  this.characters = [];
  this.entities = [];
  this.room_contents = [];
  var w = window.innerWidth;
  var h = window.innerHeight;

  this.draw = function (object) {
    this.ctx.drawImage(object.textureSourceElement, (object.positionX * pixelSize) - (object.offsetX),
      (object.positionY * pixelSize) - (object.offsetY), pixelSize, pixelSize);
  };
  this.yerlestir = function (object) {
    if (typeof object === "undefined") {
      return false;
    }
    
    var i;
    for (i = 0; i < this.characters.length; i++) {
      if (this.characters[i].id == object.id) {
        return true;
      }
    }

    if (object.constructor.name == "Character" || object.constructor.name == "Player" || object.constructor.name == "NPC") {
      this.characters.push(object);

      var nick = document.createElement('p');
      nick.id = "nick_" + object.id;
      nick.disabled = true;
      nick.className = "nick";
      nick.innerHTML = object.nick;

      if (object.constructor.name == "NPC") {
        nick.style.color = "yellow";
      }
      document.getElementsByTagName('body')[0].appendChild(nick);
      //document.getElementById("nick_ulascan").disabled = true;
      document.getElementById(nick.id).disabled = true;
    }
    else if (object.constructor.name == "RoomEntity") {
      this.entities.push(object);
    }
    this.room_contents.push(object);


  };
  this.remove = function (id) {
    var removeItem = id;
    this.room_contents = $.grep(this.room_contents, function (e) {
      return e.id != id;
    });
    this.characters = $.grep(this.characters, function (e) {
      return e.id != id;
    });
    this.entities = $.grep(this.entities, function (e) {
      return e.id != id;
    });
    $("#nick_" + id).remove();
    $("#toolTip_" + id).remove();
  };

  this.removeALL = function () {

    for (k = 0; k < this.room_contents.length; k++) {
      //console.log(this.room_contents[k]);
      //console.log(this.room_contents[k].id);
      $("#nick_" + this.room_contents[k].id).remove();
      $("#toolTip_" + this.room_contents[k].id).remove();
    }

    this.room_contents = [];
    this.characters = [];
    this.entities = [];
  }

  this.getRoomContent = function (id) {
    for (let room_content in this.room_contents) {
      if (this.room_contents[room_content].id == id)
        return this.room_contents[room_content];
    }
    return false;
  };

  var lastRender = new Date;
  this.render = function () {
    var now = new Date;
    var deltaTime = now - lastRender;
    lastRender = now;

    var sortedCharacters = this.characters.sort(function (a, b) {
      var keyA = a.positionY,
        keyB = b.positionY;

      if (keyA < keyB) return -1;
      if (keyA > keyB) return 1;
      return 0;
    });

    for (let beUpdateObject in this.room_contents) {
      this.room_contents[beUpdateObject].update(deltaTime);
    }

    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    for (let beDrawnObject in this.entities) {
      this.draw(this.entities[beDrawnObject]);
    }
    for (let beDrawnObject in sortedCharacters) {
      this.draw(this.characters[beDrawnObject]);
    }
  };

  this.click = function (clickedX, clickedY) {
    var mergedArray = this.characters.concat(this.entities);
    for (var i in mergedArray) {
      var content = mergedArray[i];
      var offsetDiffX = 0;
      var offsetDiffY = 0;

      if (content.offsetX != 0) {
        offsetDiffX = 1 / (pixelSize / content.offsetX);
      }
      if (content.offsetY != 0) {
        offsetDiffY = 1 / (pixelSize / content.offsetY);
        console.log(offsetDiffX, offsetDiffY);
      }

      var calcX = Math.abs(content.positionX - (clickedX - 0.5 - offsetDiffX));
      //  console.log(calcX,content.offsetY);
      var calcY = Math.abs(content.positionY - (clickedY - 0.5 + offsetDiffY));

      if (calcX < 0.5 && calcY < 0.5) {
        console.log(content.skin, "'a tıklandı!");
        content.onclick();
        break;
      }
    }
  };
}
