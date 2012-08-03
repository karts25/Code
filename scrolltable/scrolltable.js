function ScrollTable(rows,cols)
{
    var table = document.createElement('TABLE');
    table.style.border = "thick solid #000000";
    table.rules = "all"
    var header = table.createTHead();    
    var row,cell;
    for (i = 0; i < rows; i++)
    {
	row = header.insertRow(i);
	for(j = 0; j < cols; j++)
	{
	    cell = row.insertCell(j);
	    cell.innerHTML = '<div style="height:120px;width:120px;border:0 #ccc;font:16px/26px Georgia, Garamond, Serif;overflow:auto;"> Insert text here </div>'; 
	}
    }

    document.getElementById("para").innerHTML = "newpara";
    return table;
}
