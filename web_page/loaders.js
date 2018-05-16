function loadMapImage(name, directory, callback) {
  var dir = directory;
  var img = new Image();
  var url = dir + "/" + name + ".png?x=" + Math.random().toString(36).substring(4);
  img.onload = function () {
    callback(img);
  };
  img.src = url;
}
function entityForLoad(entityName) {
  loadMapImage(entityName, "entities", function (image) {
    $(image).attr("id", "texture_entity_" + entityName);
    $('#gameSource').append(image);
  });
}

function charactersForLoad(characterName) {
  loadMapImage(characterName, "characters", function (image) {
    $(image).attr("id", "texture_character_" + characterName);
    $('#gameSource').append(image);
  });
}

function roomsForLoad(roomName) {
 
  loadMapImage(roomName, "rooms", function (image) {
    $(image).attr("id", "texture_rooms_" + roomName);
    $('#gameSource').append(image);
  });
}

var json = function () {
  $.ajaxSetup({
    async: false
  });
  var jsonTemp = null;
  $.getJSON("loaders.json", function (data) {
    jsonTemp = data;
  });
  return jsonTemp;
}();


var jsonData = json;

function ReadCharactersJson() {

  var rotationJson, animStateJson, skinJson, finalString = [];
  for (var k in jsonData.characters) {
    rotationJson = jsonData.characters[k].rotation; // ["E", "S", "W", "N"]
    animStateJson = jsonData.characters[k].animState; // ["0", "1", "2"]
    skinJson = jsonData.characters[k].skin;

    rotationJson.forEach(elementRotation => {
      animStateJson.forEach(elementAnimState => {
        finalString.push(skinJson + elementRotation + elementAnimState);
      });
    });
  }

  for (i = 0; i < finalString.length; i++) {
    charactersForLoad(finalString[i]);
  }
}
var roomTile = ["E", "S", "W", "N", "EN", "ES", "EW", "NS", "NW", "SW", "ENS", "ENW", "ESW", "NSW", "ENSW"];
var tileString = "";
function ReadRoomsJson() {
  for (var k in jsonData.rooms) {
    for (var i in roomTile) {
      tileString = roomTile[i]+jsonData.rooms[k].skin;
      roomsForLoad(tileString);
    }
  }
}
function ReadEntitiesJson() {
  for (var k in jsonData.entities) {
    entityForLoad(jsonData.entities[k].skin);
  }
}


