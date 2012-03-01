WEB_SOCKET_SWF_LOCATION = 'WebSocketMain.swf';
var $USERS_ONLNE = 0;
$(document).ready(function() {
	//Очистка инпутов
	$('#messageform input[type="hidden"]').val('');
	$('#message').val('').focus();
    var s = new io.connect('http://' + window.location.host, {
        rememberTransport: false,
        'reconnect': true,
        'reconnection delay': 1000,
        'max reconnection attempts': 10
        });
    // Постинг формы через ajax
    $("#messageform").live("keypress", function(e) {
        if (e.keyCode == 13){
            if ($.trim($('#messageform').find("textarea").val()) != "") {
                newMessage($(this),s);
            }
            return false;
        }
    });
    $(".button_blue").live("click", function(event) {
        event.preventDefault();
        if ($.trim($('#messageform').find("textarea").val()) != "") {
            newMessage($('#messageform'), s);
        }
    });
    $(document).keyup(function(e) {
        if (e.keyCode == 27) {
            $('.closer').click(); }
    });
	$('#gear-opener').hover(function(){
		$("#gear-opener .inner").show();
	}, function(){
		$("#gear-opener .inner").hide();
	});
	$('#gear-opener a').click(function(){
		$("#gear-opener .inner").hide();
	});	
	
	/**
	 * Модульное окно редактирования профиля
	 */
	 $( "#profile_editor" ).dialog({
		width: 630,
		modal: true,
		autoOpen: false,
	});
	$("#profile_edit").click(function(){
		$( "#profile_editor" ).dialog( "open" );
	});
	$("#close_profile_editor").click(function(){
		$( "#profile_editor" ).dialog( "close" );
	});

	$('#profile-save').click(function(){
		var profileForm = $('#profile-form');
		$.post('/profile', profileForm.serialize(), function(data) {
         errors = jQuery.parseJSON(data);
         if (data) {
             for (i in errors) {
                 console.log(errors[i].error);
                 console.log(errors[i].input_name);
             }
         }
         else {
             $( "#profile_editor" ).dialog( "close" );
         }
		 console.log(data);
		});
	});
/*    $('#profile_edit').click(function(){
		alert('Пока не работает');
    });*/
    $('#cite').live('click',function(){
        var form = [{name: "message", value: "/цитата"}];
        s.json.send(form);
    });
	
    $('#joke').live('click',function(){
        var form = [{name: "message", value: "/анекдот"}];
        s.json.send(form);
    });
    $('#away').live('click',function(){
        var form = [{name: "message", value: "/away"}];
        s.json.send(form);
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
        window.scrollTo(0, document.body.scrollHeight);
        $('#inbox').css({paddingBottom: '145px'});
        $('#inbox').css('visibility', 'visible');
		$('#inbox').show();
        $('#message').focus();
		
    });
    $('#private_name .closer').live('click',function(){
    	$('#private').val("");
    	$('#personal').val("");
    	$('#private_name').html("");
    	$('.clone_personal').remove();
    	//$('#inbox').css({paddingBottom: '95px'});
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
        	},2000);
        $("#sidebar_inner").append(response.user);
        $USERS_ONLNE++;
        $('#sidebar_inner').children('h6').replaceWith('<h6>Пользователи онлайн(' + $USERS_ONLNE + '):</h6>')
    }
    else if (response.type == 'user_is_out') {
        $("#inbox").append(response.html);
        $('#'+response.user_id).parent().remove();
        $USERS_ONLNE--;
        $('#sidebar_inner').children('h6').replaceWith('<h6>Пользователи онлайн(' + $USERS_ONLNE + '):</h6>')
    }
    else if (response.type == 'status') {
        //$('#' + response.user_id).next().next().text(response.status)
		setUserAwayStatus(response.user_id, response.status);
    }
    else if (response.type == 'drop_away') {
        //$('#' + response.user_id).next().next().text("")
		setUserAwayStatus(response.user_id, false);
    }
    else if (response.type == 'kick') {
        alert("Вы плохо себя вели!");
        window.location = '/auth/logout';
    }
    else {
        $USERS_ONLNE = 0;
        $("#sidebar_inner").children('.user').remove();
        for (i in response) {
            $USERS_ONLNE++;
            var status = false;
            var user_html;
            if (response[i][3]) { status = response[i][3] }
            if (response[i][4]) {
                $user_html = "<div class=user>"
                + "<a href=noscript id='" + response[i][1] + "' class='user_nik sub_id_" + response[i][1] + " gender_" + response[i][2] + "' title='личное сообщение'>"
                + response[i][0]
                + "</a>"
                + "<a target='_blank' href='" + response[i][4] + "' class=user_info title='информация о пользователе " + response[i][0] + "'>[i]</a>"
                //+ "<span class=\"alignright\">" + status + "</span>"
                + "</div>"
                }
            else {
                $user_html = "<div class=user>"
                + "<a href=noscript id='" + response[i][1] + "' class='user_nik sub_id_" + response[i][1] + " gender_" + response[i][2] + "' title='личное сообщение'>"
                + response[i][0]
                + "</a>"
                + "</div>"
            }

            $("#sidebar_inner").append($user_html);
			setUserAwayStatus(response[i][1], status);
        }
    }
	$('html, body').animate({scrollTop: document.body.scrollHeight}, 1000);
	$('#inbox').css('visibility', 'visible');
	$('#message').focus();
}

function setUserAwayStatus(user_id, status) {
	if (status)
		$('#' + user_id).parents('.user').addClass('away');
	else
		$('#' + user_id).parents('.user').removeClass('away');
}
