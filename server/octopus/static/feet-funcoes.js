$(document).ready(function(){
	
	$("#close-code").click(function(){
		$("#code-box").slideToggle();
	});
	$("#novo-foot").click(function(){
		if($("#code-box").css("display") == 'block'){
			$("#code-input-name").val("");
			$("#code-box-textarea").text("");
			$("#code-box").slideToggle();
		};
		$("#code-box").slideToggle();
	});

	$(".foot-name").click(function(){
		var nome = $(this).attr("id");
		if($("#code-box").css("display") == 'block'){
			$("#code-input-name").val("");
			$("#code-box-textarea").text("");
			$("#code-box").slideToggle();
		};
		$.ajax({
				type: 'POST',
				url: '/find_foot', //url to submit
				data: JSON.stringify({"_id":nome}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(JsonData){	
					$("#code-box-textarea").text("");						
					$("#code-input-name").val(JsonData._id);
					$("#code-box-textarea").text(JsonData.codigo);
					$("#code-box").slideToggle();
				})
				.fail(function(JsonData){
					alert("Erro!");
		});
		
	});

	$("#save-code").click(function(){
		var nome = $("#code-input-name").val();
		var codigo = $("#code-box-textarea").val();
		console.log("Nome: "+nome+"\nCodigo: "+codigo);
		$.ajax({
				type: 'POST',
				url: '/add_foot', //url to submit
				data: JSON.stringify({"_id":nome, "codigo":codigo}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(JsonData){			
					alert(JsonData.retorno);
					$("#code-box").slideToggle();
				})
				.fail(function(JsonData){
					alert("Erro!");
		});
		
	});


});

