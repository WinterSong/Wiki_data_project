window.onload=function()
{
	var titles = document.getElementsByClassName('ptitle');
	
	for (var i = 0; i<titles.length; i++)
	{
		var obj = titles[i].nextElementSibling;
		titles[i].style.height = obj.clientHeight+'px';
	}
}