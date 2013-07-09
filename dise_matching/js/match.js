function replaceAll(txt, replace, with_this) {
  return txt.replace(new RegExp(replace,'g'),with_this);
}


function filter(value){
	
  	var disetable = document.getElementById("dise_table");
	var klptable = document.getElementById("klp_table");
	var ele;
	
	
	for(var i=1;i<disetable.rows.length;i++){
		ele=disetable.rows[i].innerHTML.replace(/<[^>]+>/g,"|").split("|")[3];
		res=ele.toLowerCase().match(value.toLowerCase());
		if(res==value.toLowerCase()){
			disetable.rows[i].style.display='';
		}
		else{
			disetable.rows[i].style.display='none';
		}
	}

	for(var i=1;i<klptable.rows.length;i++){
		ele=klptable.rows[i].innerHTML.replace(/<[^>]+>/g,"|").split("|")[3];
		res=ele.toLowerCase().match(value.toLowerCase());
		if(res==value.toLowerCase()){
			klptable.rows[i].style.display='';
		}
		else{
			klptable.rows[i].style.display='none';
		}
	}
}

function clicks(value,type){
	if(type==1){
		var table=document.getElementById('dise_table');
		for(var i=0;i<=table.rows.length-1;i++){
			table.rows[i].bgColor='#FFFFFF';
		}	
	} else {
		table=document.getElementById('klp_table');
		for(var i=0;i<=table.rows.length-1;i++){
			table.rows[i].bgColor='#FFFFFF';
		}
	}				
	if(value.bgColor=='#FFD700'){
	 	value.bgColor='#FFFFFF';
		if(type==1){
			var dise=document.getElementById('dise_value');
			dise.value='';
		
		}
		else{
			var klp=document.getElementById('klp_value');
			klp.value='';
		
		}	
	
	}
	else
	{
	 	value.bgColor='#FFD700';
		if(type==1){
			
			
			var dise=document.getElementById('dise_value');
			value_list= replaceAll(value.innerHTML,"<td>","");
			value_list= replaceAll(value_list,"</td>","|");
			value_list= value_list.substring(0,value_list.length-2);
                        //alert(value_list);
			value_list= value_list.split("|");
			dise.value=value_list.join("|");
		}
		else{
			var klp=document.getElementById('klp_value');
			value_list= replaceAll(value.innerHTML,"<td>","");
			value_list= replaceAll(value_list,"</td>","|");
			value_list= value_list.substring(0,value_list.length-2);
                        //alert(value_list);
			value_list= value_list.split("|");
			klp.value=value_list.join("|");
		}
	}
}

function myfunction()
{
	var x;
        var y=document.getElementById("dise_value").value.split("|");
	var z=document.getElementById("klp_value").value.split("|");	
	var r=confirm("Sure to match "+y[1].trim()+" and "+z[1]+" ?");
	if (r==true)
  	{
		var data=document.URL.split("/");
		document.getElementById("matched_value").value=data[data.length-2]+"|"+data[data.length-1];
		document.forms["form1"].submit();
 	 }
	else
	{
	}
}