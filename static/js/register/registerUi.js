
$(document).ready(function(){

    $(".submit-btn").click(function (e) {

        $("#msg_srt").val("");

        var src_lang = document.getElementById('language').value;
        var text = document.getElementById('msg_txt').value;

        $("#loading").show();

        var jsonObj = {
            lang: src_lang,
            text: text,
        };

        $.ajax({
            url: "/get_message",
            type: "POST",
            contentType:"application/json; charset=utf-8",
            data: JSON.stringify(jsonObj),
            dataType: "json",
            success: function (response) {
                $("#msg_srt").val(response['message']);
                $("#loading").hide();
            },
            error: function (request, response) {
                alert("Web server Error. Try again later.");
                $("#loading").hide();
                return ;
            },
            complete: function(response) {
            }
        });
    });

});


