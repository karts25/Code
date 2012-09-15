/* Functions that make life using matrices on latex more bearable
*/

function make_matrix(text)
{
    var string = text;
    var rows = string.split(/[;\n\r]+/);
    var latexmatrix = "";
    for (row in rows)
    {
	var elements = rows[row].split(" ");
	for(element in elements)
	{
	    //element = parseFloat(element);
	    latexmatrix = latexmatrix + elements[element];
	    if (element < elements.length - 1)
		latexmatrix = latexmatrix + " & ";
	}
	latexmatrix = latexmatrix+"\\\\";
    }
}