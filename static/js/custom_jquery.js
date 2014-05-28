$(function(){
    var minutes;
    var seconds;
    $("#name_slug").hide();
    setInterval(function(){
        $.ajax({
            type:'get',
            url: '/get-time/',
            success: function(data){
                minutes = Math.floor(data / 60)
                seconds = Math.floor(data % 60)
                if(seconds<10){
                    seconds = "0"+seconds
                }
                if(minutes<10){
                    minutes = "0"+minutes
                }
                $("#timer").html(minutes + " : " + seconds)
                if(data > $("#exam_time").html() * 60 ){
                 window.location = "/exam/"+$("#name_slug").html()+"/"
                }
            },
            failure:function(data){
                $("#timer").html(data);
            }
        });

        //$("#timer").html(minutes + " : " + seconds)

    } , 0, 1000);

});