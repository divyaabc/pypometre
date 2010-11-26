

<script language="JavaScript">


function point_it(event){
    nbColumns = 11;
    nbLines = 11;
    zoom = 2;
    jsondata = window['jsondata'];
    var matrix = jsondata['matrix']; 
    var colors = jsondata['colors']; 
    var fileNames = jsondata['fileNames'];
    var shortcuts = fileNames.slice();
    for(var f = 0; f < fileNames.length; f++) {
        var parts = fileNames[f].split('/');
        shortcuts[f] = parts[parts.length-1];
        parts = shortcuts[f].split('.');
        shortcuts[f] = parts[0];
    }
    var pos_x = event.offsetX?(event.offsetX):event.pageX-document.getElementById("pointer_div").offsetLeft;
    var pos_y = event.offsetY?(event.offsetY):event.pageY-document.getElementById("pointer_div").offsetTop;
    var doc_x = Math.floor(pos_x / zoom);
    var doc_y = Math.floor(pos_y / zoom);
    var matrixSize = matrix.length; 
    var nbLines = nbLines < matrixSize ? nbLines : matrixSize;
    var nbColumns = nbColumns < matrixSize ? nbColumns : matrixSize;
    var decal_x = Math.floor(nbColumns / 2);
    var decal_y = Math.floor(nbLines / 2);
    var start_x = doc_x - decal_x;
    var start_y = doc_y - decal_y;
    if (start_x > matrixSize-nbColumns) { start_x = matrixSize-nbColumns};
    if (start_x < 0) { start_x = 0;};
    if (start_y > matrixSize-nbLines) { start_y = matrixSize-nbLines};
    if (start_y < 0) { start_y = 0;};
    var tableContent = '<table border="1">';
    for (var j = 0; j < nbLines; j++) {
        tableContent += '<tr>';
        for (var i = 0; i < nbColumns; i++) {
            color = colors[start_y+j][start_x+i];
            //tableContent += '<td style="background-color:' + color + '">' + matrix[start_y+j][start_x+i];
            tableContent += '<td bgcolor="' + color + '">' + matrix[start_y+j][start_x+i];
        }
        tableContent += '<th bgcolor="#F0F8FF" align="left">' + shortcuts[start_y+j];
        tableContent += '<th bgcolor="#F0F8FF" align="left">' + fileNames[start_y+j];
    }
    tableContent += '<tr>';
    for (var i = 0; i < nbColumns; i++) {
        tableContent += '<th bgcolor="#F0F8FF">' + shortcuts[start_x+i];
    }
    tableContent += '</table>';
    document.getElementById('scores').innerHTML = tableContent;
    
}

function ajaxRequest(){
 var activexmodes=["Msxml2.XMLHTTP", "Microsoft.XMLHTTP"] //activeX versions to check for in IE
 if (window.ActiveXObject){ //Test for support for ActiveXObject in IE first (as XMLHttpRequest in IE7 is broken)
  for (var i=0; i<activexmodes.length; i++){
   try{
    return new ActiveXObject(activexmodes[i]);
   }
   catch(e){
    //suppress error
   }
  }
 }
 else if (window.XMLHttpRequest) // if Mozilla, Safari etc
  return new XMLHttpRequest();
 else
  return false;
}

var mygetrequest=new ajaxRequest();
mygetrequest.onreadystatechange=function(){
  if (mygetrequest.readyState==4){
    if (mygetrequest.status==200 || window.location.href.indexOf("http")==-1){
      var jsondata = eval("("+mygetrequest.responseText+")")
      window['jsondata'] = jsondata;
    }
  }
};
mygetrequest.open("GET", "<?php echo $_GET['name']?>.json", true);
mygetrequest.send(null);

</script>

<body>
<div id="pointer_div" onclick="point_it(event)"> <img src="<?php echo $_GET['name']?>.png"> </div>
<div id="scores"  style="width:400px;height:400px;"> </div>


