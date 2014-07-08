$(document).ready(function(){
	
	$(".vm-action").change(function(){
		var option = $(this).find(":selected").text();
		var act = $(this).find(":selected").val();
		var nome = $(this).attr("id");
		if(!confirm("Você tem certeza que deseja "+option+" a maquina?")){
			return;
		}
		$.ajax({
				type: 'POST',
				url: '/vm_action', //url to submit
				data: JSON.stringify({"vm":nome, "action":act}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(JsonData){			
					alert(JsonData.retorno);
					window.location.reload();
				})
				.fail(function(JsonData){
					alert("Erro!");
		});		
	});

	$(".acessar_console").click(function(){
		var nome = $(this).attr("id");
		if(!confirm("Você tem certeza que deseja acessar o console da maquina "+nome+" ?")){
			return;
		}
		$.ajax({
				type: 'POST',
				url: '/access_console', //url to submit
				data: JSON.stringify({"vm":nome}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(JsonData){			
					if(JsonData.retorno){
						alert("Voce precisa ter o spicy instalado: spicy -h ip_hypervisor -p "+JsonData.retorno);
					}else{
						alert("Erro! Talvez a maquina esteja desligada");
					}

					window.location.reload();
				})
				.fail(function(JsonData){
					alert("Falhou! contate o admin de sistemas!");
		});		
	});

});

