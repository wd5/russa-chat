WEB_SOCKET_SWF_LOCATION = 'WebSocketMain.swf';
var $USERS_ONLNE = 0;
var $MESSAGE_TO;
var $MESSAGE_TO_S;
$(document).ready(function() {
	//Очистка инпутов
	$('#messageform input[type="hidden"]').val('');
	$('#message').val('').focus();
    var s = new SockJS('http://' + window.location.host);
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
		 $('.profile-err').hide();
		 if (data) {
			for (var i = 0; i < errors.length; i++){
				 fn_chat_profileErr(errors[i].input_name,errors[i].error);
			}
         }
         else {
             $( "#profile_editor" ).dialog( "close" );
         }
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
    $("#inbox a.user_nik").live("click", function(event) {
        $MESSAGE_TO_S = false;
        event.preventDefault();
        var tar_id = $(this).attr('id');
            if (($MESSAGE_TO == tar_id)||($(this).parent().parent().parent().hasClass('private'))) {
                // Добавляю в инпут private значение id кому сообщение
                $('#private').val($(this).attr('id'));
                // Очищаю инпут обращения
                $('#personal').val("");
                // Не знаю что это
                // $('.clone_personal').remove();
                $('#private_name').html('<span class="closer"></span><div>Личное сообщение для '+$(this).text()+'</div>').addClass('private');
                $MESSAGE_TO = false;

        }else{
            // Очищаю инпут привата
            $('#private').val("");
                // Добавляю в инпут к кому идет обращение
                $('#personal').val(tar_id);
                $('#private_name').html('<span class="closer"></span><div>Обращение к '+$(this).text()+'</div>').removeClass('private');
                $MESSAGE_TO = tar_id;
        }
        window.scrollTo(0, document.body.scrollHeight);
        $('#inbox').css({paddingBottom: '145px'});
        $('#inbox').css('visibility', 'visible');
        $('#inbox').show();
        $('#message').focus();

    });
    $("#sidebar_inner a.user_nik").live("click", function(event) {
        if ($MESSAGE_TO) {
            $('#private').val("");
            $('#personal').val("");
            $('#private_name').html("");
            $('.clone_personal').remove();
            $MESSAGE_TO = false;
        }
        event.preventDefault();
        var tar_id = $(this).attr('id');
        if ($MESSAGE_TO_S == tar_id) {
            $('#private').val($(this).attr('id'));
            $('#personal').val("");
            $('.clone_personal').remove();
            $('#private_name').html('<span class="closer"></span><div>Личное сообщение для '+$(this).text()+'</div>').addClass('private');
            $MESSAGE_TO_S = false
        }else{
            $('#private').val("");
            var list = new Array();
            // Нужно проверить tar_id на наличие в clone_personal и personal
            if ($('#personal').attr('value').length) {
                list.push(($('#personal').attr('value')));
            }
            if ($('.clone_personal').attr('value')) {
                list.push(($('.clone_personal').attr('value')));
            }
            // Если поле привата пусто или наоборот если есть приват а также если в обращении уже есть такой чувак
            if((!($('#private_name div').length))||($('#private_name').hasClass('private'))||(!((jQuery.inArray(tar_id,list)) == -1))){
                $('#personal').val(tar_id);
                $('#private_name').html('<span class="closer"></span><div>Обращение к '+$(this).text()+'</div>').removeClass('private');
                $('.clone_personal').remove();
                $MESSAGE_TO_S = tar_id;
            }else{
                if(!($('#sidebar_inner #'+(tar_id)).hasClass('personal_link'))){
                    $('#private_name div').append(', '+$(this).text());
                    $('#messageform').append('<input class="clone_personal" id="personal" type="hidden" value="'+(tar_id)+'" name="personal[]">');
                    $MESSAGE_TO_S = tar_id;
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
        $MESSAGE_TO = false;
        $MESSAGE_TO_S = false;
    });

    s.onmessage = function(data) {
        addMessage(data.data);
    };

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

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

// Постинг сообщения в чат
function newMessage(form, s) {
    s.send(JSON.stringify(form.serializeArray()));
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
                + "<a target='_blank' href='" + response[i][4] + "' onclick='return fn_chat_userInfo(this)' class=user_info title='информация о пользователе " + response[i][0] + "'>[i]</a>"
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

function fn_chat_profileErr(input_name,error){
	
	if ($('[name="'+input_name+'"]').parents('td').find('.profile-err').html()==null){
		$('[name="'+input_name+'"]').parents('td').prepend('<div class="profile-err">'+error+'</div>');
	} else {
		$('[name="'+input_name+'"]').parents('td').find('.profile-err').html(error);
	}
	$('[name="'+input_name+'"]').parents('td').find('.profile-err').fadeIn(600);
	
}

function  fn_chat_userInfo(_this){
    if (_this.href.indexOf('profile/') !== -1) {
        $.ajax({type:"GET", url:_this.href, data:'', success: function(data){ $.fancybox(data); }});
    }
    else {
        window.open(__this.href)
    }
	
	return false;
}


