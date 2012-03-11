$(document).ready(function(){

	$('#id_login_reg').click(function(){
		$.fancybox.showActivity();
		$.ajax({type:"GET", url:'/reg', data:'', success: function(data){ $.fancybox(data); }});
		return false;
	});
	
	fn_login_testErrs();
});
function fn_reg_clickSend(_this){

	if (document.getElementById('gender_m').checked){
		document.getElementById('reg_frm_sex').value = document.getElementById('gender_m').value;
	}
	if (document.getElementById('gender_f').checked){
		document.getElementById('reg_frm_sex').value = document.getElementById('gender_f').value;
	}
	
	$.ajax({type:"POST", url:'/reg', data:fn_reg_sendData(_this.parentNode.parentNode), success: function(data){ fn_reg_result(data); }});
	
	return false;
}
function fn_reg_sendData(frm){

	if (frm == null){ return ''; }
	
	var sendData = '';
	
	var inps = new Array('input','textarea');

	for (var j = 0; j < inps.length; j++){
	
		var frm_inps = frm.getElementsByTagName(inps[j]);
		
		for (var i = 0; i < frm_inps.length; i++){
			var name = frm_inps[i].name;
			if (name !== ''){
				sendData += ((sendData==='')?'':'&')+name+'='+encodeURIComponent(frm_inps[i].value);
			}
		}
	}
	return sendData;
}
function fn_reg_result(data){
	
	$('.form-err').hide();
	if (data.indexOf('<!doctype html')== -1){ fn_reg_err(data); return; }
	//ok
	window.location = '/';
}
function fn_reg_err(data){

	var json = eval("("+data+")");
	for (var i = 0; i < json.length; i++){
		$('#error_'+json[i].input_name).html(json[i].error);
		$('#error_'+json[i].input_name).fadeIn(600);
	}
}
function fn_login_testErrs(){
	
	$('.form-err').hide();
	if (glob_input_error === ''){ return; }
	
	$('#error_lg_'+glob_input_error).html(glob_error);
	$('#error_lg_'+glob_input_error).fadeIn(600);
}

