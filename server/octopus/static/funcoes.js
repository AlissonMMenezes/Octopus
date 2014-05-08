$(document).ready(function(){
	var nodes = []
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

//	$("#input-box-title").click(function(){
//		$("#input-box-content").slideToggle();
//	});
	$(".nodes").change(function(){
			if($(this).is(":checked")){
				nodes.push($(this).attr("id"));
				$("#nodes-checked").text(nodes);
			}else{
				var i = nodes.indexOf($(this).attr("id"));
				nodes.splice(i,1);
				$("#nodes-checked").text(nodes);
			}
	});

	$("#novogrupo").click(function(){
		$("#novogrupo-nome").slideToggle();		
		if($("#novogrupo").hasClass("novogrupo-clicado")){
			$("#novogrupo").removeClass("novogrupo-clicado");	
		}else{
			$("#novogrupo").addClass("novogrupo-clicado");	
		}
		
	});

	$("#btn-cadastrar-grupo").click(function(){
		var nome = $("#nome-grupo").val();
		$.ajax({
				type: 'POST',
				url: '/novo_grupo', //url to submit
				data: JSON.stringify({"_id":nome}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(JsonData){			
					$("#notify_texto").text(JsonData.retorno);
					$("#notify").slideToggle();
					$("#notify").delay(900);
					$("#notify").slideToggle();
				})
				.fail(function(JsonData){
					$("#notify").text("falhou");
					$("#notify").slideToggle();
					$("#notify").delay(300);
					$("#notify").slideToggle();
		});
		
	});

	$(".grupos-nome").click(function(){
		$(".grupo-nome-"+$(this).attr("id")).slideToggle();
	})

	$("#btn").click(function(){
		var n = $("#node").val();
		var c = $("#comando").val();
		var p = $("#args").val();
		console.log(n+c+p)
		$.ajax({
				type: 'POST',
				url: '/comando', //url to submit
				data: JSON.stringify({"nodes":nodes,"command":c,"params":p}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(JsonData){			
					$("#notify_texto").text(JsonData.retorno);
					$("#notify").slideToggle();
					$("#notify").delay(900);
					$("#notify").slideToggle();
				})
				.fail(function(JsonData){
					$("#notify").text("falhou");
					$("#notify").slideToggle();
					$("#notify").delay(300);
					$("#notify").slideToggle();
		});



	});

});

