var host = window.location.hostname;
var port = 8888

var socket = io.connect('http://' + host + ':' + port);

socket.on('connect', function () {
    socket.emit('connected');
})

socket.on('dungeons', function (data) {
    console.log("dungeons", data);
});

socket.on('characters', function (data) {
    console.groupCollapsed("characters");
    console.log(data);
    for (k = 0; k < data.length; k++) {
        console.log(data[k].name);
        var entities;
        if (data[k].type == "player") {
            entities = new Player(data[k].id, data[k].skin, data[k].x, data[k].y, data[k].name);
        }
        else if (data[k].type == "npc") {
            entities = new NPC(data[k].id, data[k].skin, data[k].x, data[k].y, data[k].name);
        }
        Groom.yerlestir(entities);
    }
    console.groupEnd();
});

socket.on('load_room_data', function (data) {

    Groom.removeALL();
    console.groupCollapsed("load_room_data");
    console.log(data);

    var mapPortList = data.ports.sort();
    var mapNameString = "";
    for (k in mapPortList) {
        mapNameString += mapPortList[k];
    }
    mapNameString += data.thema;
    console.log("room data loaddayiz ", mapNameString);
    setMapImage(mapNameString);
    console.log(mapNameString);
    var obj = $.parseJSON(data["room_objects"]);
    for (k = 0; k < obj.length; k++) {
        console.log(obj[k].name);
        entities = new RoomEntity(obj[k].id, obj[k].name, obj[k].x, obj[k].y);
        Groom.yerlestir(entities);
    }
    console.groupEnd();
    $("#myModal").css("display", "none");
});

socket.on('spawn', function (data) {
    console.log("spawn", data);
    var p = new Player(data.id, data.skin, data.x, data.y, data.name);
    Groom.yerlestir(p)
});

socket.on('despawn', function (id) {
    console.log("despawn", id);
    Groom.remove(id);
});

socket.on('move', function (data) {
    //console.log("move", data);
    Groom.getRoomContent(data["id"]).moveTo(data["x"], data["y"], data["t"]);
});

socket.on('speech', function (data) {
    console.log("speech", data);
    addMessage(data["message"], data["id"]);
    Groom.getRoomContent(data["id"]).speech(data["message"]);
});

socket.on('ask', function (data) {
    console.log("ask", data);
    $("#myModal").css("display", "block");
    console.log(data.question);
    document.getElementById("questionText").innerHTML = data.question;
});

socket.on('answer_result', function (data) {
    console.log("answer_result", data);

    if(data > -1){
        $("#sendAnswer").css("color", "red");
        $("#sendAnswer").prop("disabled", true);
        var sayac = 10;
        var cezaText = document.getElementById("cezaText");
        cezaText.innerHTML = "Yanlis cevap! Cezanın bitmesine : 10";
        $("#cezaText").css("display", "block");
        var ceza = setInterval(function () {
            if (sayac <= 1) {
                breakInterval(ceza);
            }
            else {
                sayac--;
                cezaText.innerHTML = "Yanlis cevap! Cezanın bitmesine : " + sayac;
            }
        }, 1000);
    }
    else{
        $("#myModal").css("display", "none");
    }
    
});


function isGameReady() {
    return typeof Groom !== 'undefined'
}

function gameReady() {
    var nick = "";
    var skin = "";
    nick = $.cookie("nick");
    skin = $.cookie("skin");
    if (!nick) {
        nick = "Misafir_" + Math.random().toString(36).substring(7);
    }
    if (!skin) {
        skin = "tospik";
    }
    socket.emit("dungeons"); // dungeonları iste
    socket.emit("set_user_info", { "nick": nick, "skin": skin }); //dungeonda girmeden önce kullanılmalı
    socket.emit("join_dungeon", 0); //dungeona gir
    //artık bu ikisi bi odaya girince kendiliginden gelicek
    //socket.emit("load_room_data"); //room_contentları iste
    //socket.emit("get_characters"); //karakterleri iste
    //socket.emit("answer", "sorunun cevabi") // soruyu cevapla
}

$(document).ready(function () {
    var gameReadyChecker = setInterval(function () {
        if (isGameReady()) {
            clearInterval(gameReadyChecker);
            gameReady()
        }
    }, 500)
});