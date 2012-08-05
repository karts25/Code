function ScrollTable(rows,cols,Titles)
{
    var table = document.createElement('TABLE');
    table.style.border = "thick solid #000000";
    table.rules = "all"
    var header = table.createTHead();    
    var row,cell;    
    // insert a first row to handle sorting/selecting    
    
    row = header.insertRow(0);
    for(i = 0; i < cols; i++)
    {
	cell = row.insertCell(i);
	cell.innerHTML = '<b>'+Titles[i]+'</b>';
    }
    row = header.insertRow(1);
    for(i = 0; i < cols; i++)
    {
	cell = row.insertCell(i);
	cell.innerHTML = 'Select <form action=""> <select name="cars"> <option value="volvo">Volvo</option> <option value="saab">Saab</option> <option value="fiat">Fiat</option> <option value="audi">Audi</option> </select> </form>'
    }

    for (i = 2; i < rows+2; i++)
    {
	row = header.insertRow(i);
	for(j = 0; j < cols; j++)
	{
	    cell = row.insertCell(j);
	    cell.innerHTML = '<div style="height:120px;width:120px;border:0 #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;"> Insert text here </div>'; 
	}
    }
    
    document.getElementById("para").innerHTML = "newpara2";
    return table;
}


function insertnewRow(table,data,position = -1) // -1 denotes at end
{
    var row = table.THEAD.insertRow(position);
    for (i = 0; i < data.length; i++)
    {
	cell = row.insertCell(i);
	cell.innerHTML = data[i];
    }
}

