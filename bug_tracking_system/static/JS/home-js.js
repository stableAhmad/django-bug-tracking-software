var element = document.getElementById("navbarTogglerDemo01");
  element.style.fontSize ="100%"

 element = document.getElementById("go_projects");
  element.style.fontSize ="130%"

function expand_descrption()
{
	var Des_button_col = document.getElementsByClassName("Description")
var Des_content_col = document.getElementsByClassName("des_content")

function handler (col , i)
{
	col[i].style.display = "block"
}

for(var i = 0 ; i<Des_button_col.length ; i++)
{
	
	Des_button_col[i].addEventListener("click",(event)=>
	{
		target_content = document.getElementById(event.target.id+"c")
		if(target_content.style.display == "block")
		{
			target_content.style.display="none"
			
		}else
		{
			
		
			target_content.style.display="block"
			
			
		}
		
	})
}

}



expand_descrption()