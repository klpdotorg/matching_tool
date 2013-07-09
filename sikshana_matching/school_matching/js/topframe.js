
function callpage(value){
	var klp=document.getElementById("klp_clst");
	var sikshana=document.getElementById("sikshana_clst");

	parent.content.location.href="content/"+trim(klp.value)+"/"+trim(sikshana.value);

}

function change_focus(id,type,flag)
{
	var data='';
	var element=document.getElementById(type);
	if(type=='klp_blk')
		data=klp_blk;
	else if(type=='klp_clst')
		data=klp_clst;
	else if(type=='sikshana_blk')
		data=sikshana_blk;
	else if(type=='sikshana_clst')
		data=sikshana_clst;
	element.length=1;
	for(var i=0;i<data.length-1;i++){
		if(trim(data[i][0])==trim(id)){
			if(flag==1)
				element.options[element.length]=new Option(data[i][2],data[i][1]);
			else{
				element.options[element.length]=new Option(data[i][1],data[i][1]);
			}
		}
	}
}

function trim(value){
//	alert(value);
	while(value[value.length-1]==' ')
		value=value.substring(0,value.length-1);
	while(value[0]==' ')
		value=value.substring(1);
//	alert(value);
	return value;
}
