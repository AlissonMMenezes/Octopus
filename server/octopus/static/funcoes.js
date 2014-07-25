$(document).ready(function(){
	var nodes = []

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
		console.log(n+c+p);
		if(nodes.length <= 0){
			alert("Voce precisa selecionar ao menos um node!");
			return;
		};
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

