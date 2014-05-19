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
					$("#node-hostname").text(node.hostname);
					$("#node-ip").text(node.ip);
					$("#node-token").text(node.token);
				})
				.fail(function(JsonData){
					alert("Falhou!");
		});
		
	});

});

