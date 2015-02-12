function filetype_chosen() {

	var inputlist = document.getElementsByClassName('uploadfile');

	for (var i = 0; i < inputlist.length; i++) {

		if (inputlist[i].checked) {

			document.getElementById(inputlist[i].value+"file").style.display="block";

		} else {

			document.getElementById(inputlist[i].value+"file").style.display="none";

		}

	}

}



function xmltype_chosen(t) {

	var i = document.getElementById('xmltype');

    i.name=t;

}



function sample(path){

	var f = document.getElementsByTagName('form')[0];

	var i = document.createElement('input');

	i.type="hidden";

	i.name="sample";

	i.value=path;

	f.appendChild(i);

	f.submit();

}


/*
function json_chosen() {

	var inputlist = document.getElementsByClassName('json');

	for (var i = 0; i < inputlist.length; i++) {

		if (inputlist[i].checked) {

			document.getElementById(inputlist[i].value+"file").style.display="block";

		} else {

			document.getElementById(inputlist[i].value+"file").style.display="none";

		}

	}

}*/

function showConfig1(){
	if(document.getElementById('iconYes').innerHTML=="► "){
		document.getElementById('iconYes').innerHTML="▼ ";
		document.getElementById('yesfile').style.display="block";
	}else{
		document.getElementById('iconYes').innerHTML="► ";
		document.getElementById('yesfile').style.display="none";
	}
}

function showConfig2(){
	if(document.getElementById('iconNo').innerHTML=="► "){
		document.getElementById('iconNo').innerHTML="▼ ";
		document.getElementById('nofile').style.display="block";
	}else{
		document.getElementById('iconNo').innerHTML="► ";
		document.getElementById('nofile').style.display="none";
	}
}

