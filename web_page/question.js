var questionObj;

function getQuestion(soru, choices) {
    this.soru = soru;
    this.choices = choices;
}
function sendAnswer(answer) {

}
function getQuestionResult(time) {
    this.time = time;
}
function breakInterval(interval) {
    clearInterval(interval);
    $('#sendAnswer').prop("disabled", false);
    $('#sendAnswer').css("color", "white");
    $("#cezaText").css("display", "none");
   
}


    console.log("geldi");
    this.soru = "";
   
    this.choices = [];
    this.time = 0;

    getQuestion("Selam!", ["2", "5", "8", "12"]);

    document.getElementById("questionText").innerHTML = this.soru;
        $("#singleChoice").css("display", "block");
    var modal = document.getElementById('myModal');

    // Get the button that opens the modal
    var btnSendAnswer = $("#sendAnswer");
    var txtAnswer = $("#AnswerText");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    $('#sendAnswer').on('click', function () {
        var answerText = $('input[name=radio-group]:checked').val();

        sendAnswer(answerText);
        getQuestionResult(-1);


        if (time < 0) {
            $(this).css("color", "red");
            $(this).prop("disabled", true);
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

    });

    // When the user clicks the button, open the modal 
  


    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
