window.onload =function(){
	var totalWidth = document.body.clientWidth;
	var contWidth = document.getElementById('searchHead').style.width;
	var realMargin = (totalWidth- 440)/2;
	document.getElementById('searchHead').style.left = realMargin.toString()+"px";
	var results = document.getElementsByClassName('result_dsc');
	for(var i = 0; i<results.length;i++)
		results[i].parentNode.style.height = results[i].clientHeight+'px';
}
