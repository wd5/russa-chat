WEB_SOCKET_SWF_LOCATION = 'WebSocketMain.swf';
var $USERS_ONLNE = 0;
var $MESSAGE_TO;
var $MESSAGE_TO_S;
var $MY_ID;
$(document).ready(function() {
    var s;
	//Очистка инпутов
	$('#messageform input[type="hidden"]').val('');
	$('#message').val('').focus();
    function connect() {
        s = new SockJS('http://' + window.location.host);
        s.onclose = onclose;
        s.onmessage = onmessage;
    }
    function onclose() {
        setTimeout(function() {
            connect();
        },3000);
    }
    connect();
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

	//-mp3 win-
	$("#mp3_win").dialog({
		width: 400,
		modal: true,
		autoOpen: false,
	});
	$("#btn_mp3_show").click(function(){
		$("#mp3_win" ).dialog("open");
		return false;
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

    $('#cite').live('click',function(){
        var form = [{name: "message", value: "/цитата"}];
        s.send(JSON.stringify(form));
    });
	
    $('#joke').live('click',function(){
        var form = [{name: "message", value: "/анекдот"}];
        s.send(JSON.stringify(form));
    });
    $('#away').live('click',function(){
        var form = [{name: "message", value: "/away"}];
        s.send(JSON.stringify(form));
    });
    //insert player
	$("#inbox").html(fn_mp3_insertPlayer($("#inbox").html()));
	//Приват
    $("a.user_nik").live("click", function(e) {
        if (e.shiftKey) {
            if ($MESSAGE_TO||$MESSAGE_TO_S) {
                $('#private').val("");
                $('#personal').val("");
                $('#private_name').html("");
                $('.clone_personal').remove();
                $('.clone_private').remove();
                $MESSAGE_TO = $MESSAGE_TO_S = false;
            }
            var tar_id = $(this).attr('id');
            if (tar_id !== $MY_ID) {
                var list = new Array();
                // Нужно проверить tar_id на наличие в clone_personal и personal
                if ($('#private').attr('value').length) {
                    list.push(($('#private').attr('value')));
                }
                if ($('.clone_private').attr('value')) {
                    if ($('.clone_private').attr('value')) {
                        var el = document.getElementsByClassName("clone_private");
                        for (var i=0, l=el.length; i<l; i++){
                            list.push(el.item(i).value);
                        }
                    }
                }
                if((!($('#private_name div').length))) {
                    // Добавляю в инпут private значение id кому сообщение
                    $('#private').val($(this).attr('id'));
                    $('#private_name').html('<span class="closer"></span><div>Личное сообщение для '+$(this).text()+'</div>').addClass('private');
                }
                else if (jQuery.inArray(tar_id, list) != -1) {
                }
                else {
                    $('#private_name div').append(', '+$(this).text());
                    $('#messageform').append('<input class="clone_private" id="private" type="hidden" value="'+(tar_id)+'" name="private">');
                }
            }
            window.scrollTo(0, document.body.scrollHeight);
            $('#inbox').css({paddingBottom: '145px'});
            $('#inbox').css('visibility', 'visible');
            $('#inbox').show();
            $('#message').focus();
        }
    });
    $("#inbox a.user_nik").live("click", function(event) {
        event.preventDefault();
        if (!event.shiftKey) {
            $MESSAGE_TO_S = false;
            var tar_id = $(this).attr('id');
            if (tar_id !== $MY_ID) {
                if (($MESSAGE_TO == tar_id)||($(this).parent().parent().parent().hasClass('c_private_message_outgoing'))) {
                        // Добавляю в инпут private значение id кому сообщение
                        $('#private').val($(this).attr('id'));
                        // Очищаю инпут обращения
                        $('#personal').val("");
                        $('.clone_personal').remove();
                        $('#private_name').html('<span class="closer"></span><div>Личное сообщение для '+$(this).text()+'</div>').addClass('private');
                        $MESSAGE_TO = false;

                }else{
                    // Очищаю инпут привата
                    $('#private').val("");
                    $('.clone_private').remove();
                    // Добавляю в инпут к кому идет обращение
                    $('#personal').val(tar_id);
                    $('#private_name').html('<span class="closer"></span><div>Обращение к '+$(this).text()+'</div>').removeClass('private');
                    $MESSAGE_TO = tar_id;
                }
            }
            window.scrollTo(0, document.body.scrollHeight);
            $('#inbox').css({paddingBottom: '145px'});
            $('#inbox').css('visibility', 'visible');
            $('#inbox').show();
            $('#message').focus();
        }
    });
    $("#sidebar_inner a.user_nik").live("click", function(event) {
        event.preventDefault();
        if (!event.shiftKey) {
            if ($MESSAGE_TO) {
                $('#private').val("");
                $('#personal').val("");
                $('#private_name').html("");
                $('.clone_personal').remove();
                $MESSAGE_TO = false;
            }
            var tar_id = $(this).attr('id');
            if (tar_id !== $MY_ID) {
                if ($MESSAGE_TO_S == tar_id) {
                    $('#private').val($(this).attr('id'));
                    $('#personal').val("");
                    $('.clone_personal').remove();
                    $('#private_name').html('<span class="closer"></span><div>Личное сообщение для '+$(this).text()+'</div>').addClass('private');
                    $MESSAGE_TO_S = false
                }else{
                    $('#private').val("");
                    $('.clone_private').remove();
                    var list = new Array();
                    // Нужно проверить tar_id на наличие в clone_personal и personal
                    if ($('#personal').attr('value').length) {
                        list.push(($('#personal').attr('value')));
                    }
                    if ($('.clone_personal').attr('value')) {
                        if ($('.clone_private').attr('value')) {
                            var el = document.getElementsByClassName("clone_personal");
                            for (var i=0, l=el.length; i<l; i++){
                                list.push(el.item(i).value);
                            }
                        }
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
            }
        window.scrollTo(0, document.body.scrollHeight);
        $('#inbox').css({paddingBottom: '145px'});
        $('#inbox').css('visibility', 'visible');
        $('#inbox').show();
        $('#message').focus();
        }
    });
    $('#private_name .closer').live('click',function(){
    	$('#private').val("");
    	$('#personal').val("");
    	$('#private_name').html("");
    	$('.clone_personal').remove();
        $('.clone_private').remove();
    	//$('#inbox').css({paddingBottom: '95px'});
    	$('.personal_link').removeClass('personal_link');
        $MESSAGE_TO = false;
        $MESSAGE_TO_S = false;
    });

    function onmessage(data) {
        addMessage(data.data);
    }

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
    s.send(JSON.stringify(form.serializeArray()));
    $('#messageform').find("textarea").val('');
    form.slideDown();
    return false;
}

function addMessage(response){

    if (response.type == 'new_message'){
	
		var $last = $(fn_mp3_insertPlayer(response.html)).appendTo("#inbox");
		
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
		/*
        setTimeout(function(){
        		$last_user.children('.shadow').animate({opacity:0},4000);
        	},2000);
		*/
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
    else if (response.type == 'your_id') {
        $MY_ID = response.user_id;
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
	
	if (document.getElementById('scroll_checkbox').checked){
		$('html, body').animate({scrollTop: document.body.scrollHeight}, 1);
	}
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

function fn_mp3_send(el) {

	var ok = true;
	var s = $('.ui-dialog').find('.inp_f').val();
	var p = s.lastIndexOf('.');
	if (p == -1){ ok = false }
	else {
		s = s.slice(p).toLowerCase();
		if (s !== '.mp3'){
			ok = false;
		}
	}
	
	if (!ok){
		alert('Допустимы файлы только с расширением ".mp3"');
		document.getElementById('mp3_form').reset();
		return;
	}
	
	$$f({formid:'mp3_form', url:'/test',
		onstart:function () {
			var sp = el.parentNode.parentNode.getElementsByTagName('span');
			sp[0].style.display = 'none';
			sp[1].style.display = 'block';
		},onsend:function() {
			var sp = el.parentNode.parentNode.getElementsByTagName('span');
			sp[1].style.display = 'none';
			sp[0].style.display = 'block';
			document.getElementById('mp3_form').reset();
			$("#mp3_win").dialog("close");
			var tag = '[audio:"'+document.getElementById('mp3_fname').innerHTML+'","'+document.getElementById('mp3_name').innerHTML.replace(/"/g,"'")+'"]';
			var s = $("#message").val();
			$("#message").val(s+' '+tag+' ');
			$("#message").focus();
			//-caret to end
			var tx = document.getElementById('message');
			if (tx.createTextRange){
				var r = tx.createTextRange();
				r.collapse(false);
				r.select();
			}
			if (tx.selectionStart){
				var end = tx.value.length;
				tx.setSelectionRange(end,end);
				tx.focus();
			}
	}});
}

var player = '<div><object width="300" height="30" data="/static/res/mini_player.swf" type="application/x-shockwave-flash">\
<param name="movie" value="/static/res/mini_player.swf" />\
<param name="flashvars" value="path_mp3=/*1*&name_mp3=*2*"/>\
<param name="wmode" value="transparent"/></object></div>';

function fn_mp3_insertPlayer(data){

	var res = '';
	var p = -1;
	var p2 = -1;
	var p0 = -1;
	for (var i = 0; i < 100; i++){
		p = data.indexOf('[audio:"',p0);
		if (p == -1){ break; }
		var p2 = data.indexOf('","',p+1);
		if (p2 == -1){ break; }
		//-fname
		var fname = data.slice(p+8,p2);
		//-
		var p3 = data.indexOf('"]',p2+3);
		if (p3 == -1){ break; }
		//-name
		var name = data.slice(p2+3,p3);
		//-insert
		res += data.slice(p0+1,p);
		res += player.replace('*1*',fname).replace('*2*',encodeURIComponent(name));
		
		//-
		p0 = p3+1;
	}
	
	res += data.slice(p0+1);
	
	return res;
}
