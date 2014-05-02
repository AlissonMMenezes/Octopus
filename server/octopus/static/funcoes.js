$(document).ready(function(){

	alert("teste");
	$("#btn").click(function(){
		alert("clickou!");
		$(".nodes").each(function(){			
			if($(this).is(":checked")){
				alert("checado!");
			}else{
				alert("nao checado!");
			}			
		});

	});

});

