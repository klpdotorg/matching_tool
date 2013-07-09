
function callpage(value){
	var dise=document.getElementById("dise_clust");
	var klp=document.getElementById("klp_clust");

	parent.content.location.href="content/"+trim(dise.value)+"/"+trim(klp.value);

}

function change_focus(id,type,flag)
{
	var data='';
	var element=document.getElementById(type);
	if(type=='dise_blk')
		data=dise_block;
	else if(type=='dise_clust')
		data=dise_clust;
	else if(type=='klp_blk')
		data=klp_block;
	else if(type=='klp_clust')
		data=klp_clust;
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
