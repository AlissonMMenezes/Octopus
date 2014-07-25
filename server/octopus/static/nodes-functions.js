$(document).ready(function(){
	$(".nodes-name").click(function(){
		var nome = $(this).attr("id");		
		$.ajax({
				type: 'POST',
				url: '/node_info', //url to submit
				data: JSON.stringify({"hostname":nome}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(node){			
					$("#node-grupo").text(node._id);
					$("#node-grupo-feet").text(node.feet);
					$("#node-hostname").text(node.nodes.hostname);
					$("#node-ip").text(node.nodes.ip);
					$("#node-token").text(node.token);
					$("#node-feet-item").text(node.nodes.feet);
				})
				.fail(function(JsonData){
					alert("Falhou!");
		});
		
	});

	$("#add-foot-to-node").click(function(){
		var grupo = $("#node-grupo").text();
		var node = $("#node-hostname").text();
		var foot = $("#select-feet").find(":selected").text();
		
		if(!confirm("Realmente deseja adicionar o foot: "+foot)){
			return;
		}
		$.ajax({
				type: 'POST',
				url: '/add_foot_to_node', //url to submit
				data: JSON.stringify({"grupo":grupo,"hostname":node, "foot":foot}),
				contentType: 'application/json; charset=utf-8'
				})
				.done(function(json){								
					alert(json.retorno);
				})
				.fail(function(JsonData){
					alert("Falhou!");
		});
		
	});

});

