function Chat() {

    function speech(text, playerID) {

        var toolTipID = "toolTip_" + playerID;
        var messageID = "message_" + playerID;
        if ($("#" + toolTipID).length <= 0) {
            var toolTip = document.createElement('div');
            toolTip.id = toolTipID;
            toolTip.className = "toolTip";
            document.getElementsByTagName('body')[0].appendChild(toolTip);

            var message = document.createElement('p');
            message.id = messageID;
            message.className = "message";
            toolTip.appendChild(message);

            var tail1 = document.createElement('div');
            tail1.id = "tail1";
            toolTip.appendChild(tail1);

            var tail2 = document.createElement('div');
            tail2.id = "tail2";
            toolTip.appendChild(tail2);
        }
        $("#" + toolTipID).css("left", ((this.positionX) * (964 / 13)) + "px");
        $("#" + toolTipID).css("top", ((this.positionY - 1) * (775 / 9)) + "px");

        if ($("#" + toolTipID).is(":visible")) {
            return true;
        }
        else {
            $("#" + toolTipID).fadeIn(1000);
            var strLen = text.length;
            let text = text;
            let to = strLen,
                from = 0;

            animate({
                duration: 1000,
                timing: quad,
                draw: function (progress) {
                    let result = (to - from) * progress + from;
                    $("#" + messageID).text(text.substr(0, Math.ceil(result)));
                }
            });

            //   $("#backP").append("Player : "+text + "</br>");
        }
        setTimeout(
            function () {
                $("#" + toolTipID).fadeOut(500);
            }, 5000);
        $("#" + messageID).text("");
        function quad(timeFraction) {
            return Math.pow(timeFraction, 2)

        }
        //    $("#message").text($("#textArea").val());
        //    $("#toolTip").fadeToggle(1000);    
    }

}
