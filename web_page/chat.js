var addMessage;
$(document).ready(function () {

    var list = $("#hd-chat-messages");
    list.mCustomScrollbar({ theme: "game-default" });
    list.mCustomScrollbar('scrollTo', 'bottom');

    addMessage = function (text, id) {
        var messageH5 = document.createElement('h5');
        messageH5.innerHTML = "<span  style='color:lightblue;'>" + Groom.getRoomContent(id).nick + " :</span> " + text;
        Groom.getRoomContent(id).speech(text);
        list.mCustomScrollbar('scrollTo', 'last');
        document.getElementById('mCSB_1_container').appendChild(messageH5);
    }

    function sendMessage(text) {
        if ($("#toolTip_p1").is(":visible")) {
            return true;
        }
        else {
            socket.emit("speech", text);
        }
    }

    $("#hd-chat-send").click(function (e) {
        sendMessage($("#inputText").val());
        $("#inputText").val("");
    });
    $("#inputText").keypress(function (event) {
        if (event.which == 13) {
            event.preventDefault();
            sendMessage($("#inputText").val());
            $("#inputText").val("");
        }
    });
});