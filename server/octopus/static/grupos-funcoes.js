$(document).ready(function(){

	$(".ul-sortable-list").sortable({
		connectWith: ".ul-sortable-list"
	});
	
	$("#btn-cadastrar-grupo").click(function(){
		var nome = $("#nome-grupo").val();
		if (nome == ""){
			alert("O nome do grupo não pode ser nulo!");
			return;
		}
		$.ajax({
				type: 'POST',
				url: '/new_group', //url to submit
				data: JSON.stringify({"_id":nome}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(JsonData){			
					alert(JsonData.retorno);
					window.location.reload();
				})
				.fail(function(JsonData){
					alert("Falhou!");
		});
		
	});

	$(".excluir-grupo").click(function(){
		var nome = $(this).attr("id");
		
		var resp = confirm("Tem certeza que deseja excluir o grupo "+nome+" ?");
		if(resp != true){ return }
		$.ajax({
				type: 'POST',
				url: '/delete_group', //url to submit
				data: JSON.stringify({"_id":nome}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(JsonData){			
					alert(JsonData.retorno);
					window.location.reload();
				})
				.fail(function(JsonData){
					alert("Falhou!");
		});		
	});

	$("#add-foot-to-group").click(function(){
		var grupo = $("#grupos-box-content ul").attr("id");
		var foot = $("#select-feet").find(":selected").text();
		if(!confirm("Realmente deseja adicionar o foot: "+foot)){
			return;
		}
		$.ajax({
				type: 'POST',
				url: '/add_foot_to_group', //url to submit
				data: JSON.stringify({"grupo":grupo, "foot":foot}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(json){								
					alert(json.retorno);
					window.location.reload();
				})
				.fail(function(JsonData){
					alert("Falhou!");
		});
		
	});

	$("#remove-foot-from-group").click(function(){
		var grupo = $("#grupos-box-content ul").attr("id");
		var foot = $("#select-feet").find(":selected").text();
		if(!confirm("Realmente deseja remover o foot: "+foot)){
			return;
		}
		$.ajax({
				type: 'POST',
				url: '/remove_foot_from_group', //url to submit
				data: JSON.stringify({"grupo":grupo, "foot":foot}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(json){								
					alert(json.retorno);
					window.location.reload();
				})
				.fail(function(JsonData){
					alert("Falhou!");
		});
		
	});


});

