$(document).ready(function(){
//	$.ajax({
//				type: 'POST',
//				url: '/output', //url to submit
//				data: JSON.stringify({'maquina':'vmteste','comando':'hostname','args':'-i'}),
//				contentType: 'application/json; charset=utf-8'
//				})
//				.done(function(JsonData){				
//					console.log(JsonData);
//				})
//				.fail(function(JsonData){
//					alert("falhou");
//					console.log(JsonData);
//		});


	$("#btn").click(function(){
		var j = $.parseJSON($("#com_json").val());
		console.log(j);
		$.ajax({
				type: 'POST',
				url: '/comando', //url to submit
				data: JSON.stringify(j),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(JsonData){				
					alert(JsonData.retorno);
				})
				.fail(function(JsonData){
					alert("falhou");
					console.log(JsonData);
		});



	});

});

