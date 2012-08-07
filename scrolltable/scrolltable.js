/*
  Create a ScrollTable. 
  Arguments: rows,cols = # of rows,cols
             Titles = Array of Titles of each column
	     Options = Array of Optins ('Select' or 'None')
*/

function ScrollTable(rows,cols,Titles,Options)
{       
    MyScrollTable = new Object();
    MyScrollTable.Options = Options;
    MyScrollTable.rows = rows;
    MyScrollTable.cols = cols;
    MyScrollTable.keys = new Array(cols);
    for(i = 0; i< cols; i++)
    {
	MyScrollTable.keys[i] = new Array();
    }
    var table = document.createElement('TABLE');
    MyScrollTable.table = table
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
	if (Options[i] == "Select")
	{	    
	    cell.innerHTML = '<select id="Select'+i+'" onchange = MyScrollTable.selectRows(this,'+i+') > <option> All </option> </select> </form>';
	    var inner = cell.innerHTML;
	}
	else
	    cell.innerHTML = "None";
    }
        
    MyScrollTable.insertRow = insertRow;   
    MyScrollTable.addKeys = addKeys;
    MyScrollTable.selectRows = selectRows;
    document.getElementById("para").innerHTML = "new"+rows+"para2";
    return MyScrollTable;
}

function insertRow(position,data)
{
    var row;
    var k = data.length;
    if (position == -1)
	row = this.table.insertRow(position);
    else
	row = this.table.insertRow(position+2);   
    for (i = 0; i < data.length; i++)
    {	
	cell = row.insertCell(i);
	if (this.Options[i] == "Select") // add new tags
	{
	    var datastring = data[i];
	    var keys = datastring.split(",");// split on commas
	    var newkeys = new Array();
	    for (key in keys) // add this to the keys
	    {
		if (this.keys[i].indexOf(keys[key]) == -1)
		{
		    this.keys[i].push(keys[key]);	    	
		    newkeys.push(keys[key]);
		}
		// add the key to the drop down list		
	    }
	    this.addKeys(i,newkeys);
	}
    	
	cell.innerHTML = '<div style="height:120px;width:200px;border:0 #ccc;font:16px/26px Georgia,\
Garamond, Serif;overflow:auto;">'+data[i]+'</div>';
    }    
}

function addKeys(column,keys)
{    
    var html_newkeys="";
    for (key in keys)
	html_newkeys = html_newkeys + " <option> " + keys[key] + " </option>";
    var form_html = this.table.rows[1].cells[column].innerHTML;    
    var pos = form_html.search("</select>");
    html_newkeys = html_newkeys + " </select>";
    form_html = form_html.replace("</select>", html_newkeys);    
    this.table.rows[1].cells[column].innerHTML = form_html;
}
function selectRows(form,col)
{    
    var k = col;
    var sel_index = form.selectedIndex;
    var selection = form.options[sel_index].value;   
    // now hide all rows except those that fit the tag
    var rows = this.table.rows    
    for (i = 2; i< rows.length; i++)
    {
	if (selection == "All")
	    this.table.rows[i].style.display = "";
	else
	{
	    var cells = rows[i].cells;
	    var data = cells[col].children[0].childNodes[0].data;
	    if (data.search(selection) == -1)
		this.table.rows[i].style.display = "none";	
	    else
		this.table.rows[i].style.display = "";
	}
    }	        
    document.getElementById("para").innerHTML = col;
}

