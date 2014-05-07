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
		var n = $("#node").val();
		var c = $("#comando").val();
		var p = $("#args").val();
		console.log(n+c+p)
		$.ajax({
				type: 'POST',
				url: '/comando', //url to submit
				data: JSON.stringify({"node":n,"command":c,"params":p}),
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

