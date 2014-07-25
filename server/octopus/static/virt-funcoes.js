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
					if(JsonData.hostname){
						alert("Voce precisa ter o spicy instalado: spicy -h "+JsonData.hostname+" -p "+JsonData.port);
					}else{
						alert("Erro! Talvez a maquina esteja desligada");
					}

					window.location.reload();
				})
				.fail(function(JsonData){
					alert("Falhou! contate o admin de sistemas!");
		});		
	});

	function get_net(){		
		$.ajax({
				type: 'POST',
				url: '/get_networks', //url to submit
				data: JSON.stringify({"network":"default"}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(JsonData){			
					console.log(JsonData.retorno);
					$("#nome-rede").text(JsonData.retorno.name[1]);
					$("#ip-rede").text(JsonData.retorno.ip[0].address);
					$("#bridge-rede").text(JsonData.retorno.bridge[0].name);
					$("#range-rede").text(JsonData.retorno.range[0].start+" - "+JsonData.retorno.range[0].end);
					//$("#nome-rede").text(JsonData.retorno.range[0].end);
				})
				.fail(function(JsonData){
					alert("Falhou! contate o admin de sistemas!");
				});		
	};

	$(".virt-menu-item").click(function(){
		$(".sect").hide();
		switch($(this).attr("id")){
			case 'vm-menu':
				$('#main').show();				
				break;
			case 'net-menu':
				$('#network').show();
				get_net();
				break;
			case 'stor-menu':
				$('#storages').show();
				break;
			case 'hyper-menu':
				$('#hypervisors').show();
				break;
		}
		
		
	});

});

