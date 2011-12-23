WEB_SOCKET_SWF_LOCATION = 'WebSocketMain.swf';
$(document).ready(function() {
	//Очистка инпутов
	$('#messageform input[type="hidden"]').val('');
	$('#message').val('').focus();
    var s = new io.connect('http://' + window.location.host, {
        'reconnect': true,
        'reconnection delay': 500,
        'max reconnection attempts': 10,
        rememberTransport: false
        });
    // Постинг формы через ajax
    $("#messageform").live("keypress", function(e) {
        if (e.keyCode == 13){
            newMessage($(this),s);
            return false;
        }
    });
    $("#messageform input").live("click", function(event) {
        event.preventDefault();
        newMessage($('#messageform'), s);
    });
    $(".out_link").live("click", function() {
        s.emit('exit', 1);
    });
    //Приват
    $("a.user_nik").live("click", function(event) {
    	event.preventDefault();
    	var tar_id = $(this).attr('id');
    	if($('#'+(tar_id)).hasClass('personal_link')||($(this).parent().parent().parent().hasClass('private'))){
    		$('.personal_link').removeClass('personal_link');
    		$('#private').val($(this).attr('id'));
    		$('#personal').val("");
    		$('.clone_personal').remove();
	        $('#private_name').html('<span class="closer"></span><div>Личное сообщение для '+$(this).text()+'</div>').addClass('private');
    	}else{
    		$('#private').val("");
    		if((!($('#private_name div').length))||($('#private_name').hasClass('private'))){
    			$('#personal').val(tar_id);
    			$('#private_name').html('<span class="closer"></span><div>Обращение к '+$(this).text()+'</div>').removeClass('private');
    			$('a.sub_id_'+tar_id).addClass('personal_link');
    		}else{
    			if(!($('#'+(tar_id)).hasClass('personal_link'))){
	    			$('#private_name div').append(', '+$(this).text());
	    			$('#messageform').append('<input class="clone_personal" id="personal" type="hidden" value="'+(tar_id)+'" name="personal[]">');
	    			$('a.sub_id_'+tar_id).addClass('personal_link');
	    		}
	    	}
    	}
        $('#inbox').css({paddingBottom: '135px'});
        window.scrollTo(0, document.body.scrollHeight);
        $('#message').focus();
    });
    $('#private_name .closer').live('click',function(){
    	$('#private').val("");
    	$('#personal').val("");
    	$('#private_name').html("");
    	$('.clone_personal').remove();
    	$('#inbox').css({paddingBottom: '95px'});
    	$('.personal_link').removeClass('personal_link');
    });

    s.on('message', function(data) {
        addMessage(data);
    });

    if (/*@cc_on!@*/false) {
        document.onfocusin = function(){
            focus = "True";
        };
        document.onfocusout = function(){
            focus = "False";
        }
    } else {
        window.onload=window.onfocus = function(){
            focus = "True";
        };
        window.onblur = function(){
            focus = "False";
        }
    }
});

// Постинг сообщения в чат
function newMessage(form, s) {
    s.json.send(form.serializeArray());
    $('#messageform').find("textarea").val('');
    form.slideDown();
    return false;
}

function addMessage(response){
    if (response.type == 'new_message'){
        var $last = $(response.html).appendTo("#inbox");
        if (response.private =="True"){
            if (focus == "False"){
                document.getElementById('audiotag1').play();
                $.animateTitle(['В чате новое сообщение', '@@@@'], 500);
                $.after(4, "seconds", function() {
                    $.animateTitle("clear");
                });
             }
        }
        if (response.personal =="True"){
            if (focus == "False"){
                document.getElementById('audiotag1').play();
                $.animateTitle(['В чате новое сообщение', '@@@@'], 500);
                $.after(4, "seconds", function() {
                    $.animateTitle("clear");
                });
             }
        }
    }
    else if (response.type == 'new_user') {
        var $last_user = $(response.html).appendTo("#inbox");
        setTimeout(function(){
        		$last_user.children('.shadow').animate({opacity:0},4000);
        	},2000)
        $("#sidebar_inner").append(response.user);
    }
    else if (response.type == 'user_is_out') {
        $("#inbox").append(response.html);
        $('#'+response.user_id).remove();
    }
    else {
        $("#sidebar_inner").children('a').remove();
        for (i in response) {
            $("#sidebar_inner").append('<a id="' + response[i][1] + '" href="noscript" class="user_nik sub_id_' + response[i][1] + '" title="личное сообщение">' + response[i][0] + '</a);')
        }
    }
    window.scrollTo(0, document.body.scrollHeight);
}
