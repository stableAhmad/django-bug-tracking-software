Des_button_col = ddocument.getElementsByClassName("Description")

for(var elem of Des_button_col )
{
	elem.addEventListener("click",()=>
	{
		var key = elem.id+"c"
		rel = docuemnt.getElementById(key)
		rel.style.display ="block"
	})
}