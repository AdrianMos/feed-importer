// Script version: V2.1
//set ruler units to CM
//var orig_ruler_units = preferences.rulerUnits;
//preferences.rulerUnits = Units.CM;
//app.preferences.typeUnits = TypeUnits.POINTS
/*
var doc = app.activeDocument;

var max;

if (doc.width>doc.height)
	max = doc.width;
else
	max = doc.height;
doc.resizeCanvas(max, max, AnchorPosition.MIDDLECENTER);
doc.resizeImage(null,UnitValue(300,"px"),null,ResampleMethod.BICUBIC);
*/
// resize canvas to A4 portrait or landscape according to the ratio of activeDocument
/*if (doc.width>doc.height){ 
   activeDocument.resizeCanvas(21, 29.7, AnchorPosition.TOPCENTER);
   }else{ 
      if(width<height){
      activeDocument.resizeCanvas(20, 28.5, AnchorPosition.MIDDLECENTER);
      activeDocument.resizeCanvas(21, 29.7, AnchorPosition.BOTTOMCENTER);
   }}
   */
   
   main();
function main(){
var folders =[];
//var topLevel = Folder.selectDialog("Please select top level folder");   
//alert(topLevel)
var topLevel = Folder('C:/haiducel importuri/_ imagini noi/mici neprocesate')
if(topLevel == null ) return;
//var outPutFolder = Folder.selectDialog("Please select output folder");
var outPutFolder = Folder('C:/haiducel importuri/_ imagini noi/procesate')
if(outPutFolder == null ) return;
var max;
//get a list of all sub folders
folders = FindAllFolders(topLevel, folders);
//add selected foler
folders.unshift(topLevel);
// set up a counter
var Counter = 1;
//iterate through the folder list
for(var f in folders){
   var fileList = folders[f].getFiles();
   for(var j in fileList){
       open(fileList[j]);
// get a reference to the current (active) document and store it in a variable named "doc"
doc = app.activeDocument; 
// change the color mode to RGB. Important for resizing GIFs with indexed colors, to get better results
doc.changeMode(ChangeMode.RGB); 
// these are our values for the end result width and height (in pixels) of our image
/*var fWidth = 500;
var fHeight = 500;
// do the resizing. if height > width (portrait-mode) resize based on height. otherwise, resize based on width
if (doc.height > doc.width) {
doc.resizeImage(null,UnitValue(fHeight,"px"),null,ResampleMethod.BICUBIC);
}else {
doc.resizeImage(UnitValue(fWidth,"px"),null,null,ResampleMethod.BICUBIC);
}*/
if (doc.width>doc.height)
	max = doc.width;
else
	max = doc.height;
doc.resizeCanvas(max, max, AnchorPosition.MIDDLECENTER);
doc.resizeImage(null,UnitValue(300,"px"),null,ResampleMethod.BICUBIC);

var fileExtension = fileList[j].name.substring(fileList[j].name.lastIndexOf("."), fileList[j].name.length)
var saveFile = new File(outPutFolder+"/"+TrimFileName(fileList[j].name)+"_s" + fileExtension);


//Save document
SaveForWeb(saveFile,80);
//close the document
app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
//Increment counter
Counter++;
       }
    }

}
function FindAllFolders( srcFolderStr, destArray) {
   var fileFolderArray = Folder( srcFolderStr ).getFiles();
   for ( var i = 0; i < fileFolderArray.length; i++ ) {
      var fileFoldObj = fileFolderArray[i];
      if ( fileFoldObj instanceof File ) {         
      } else {
         destArray.push( Folder(fileFoldObj) );
      FindAllFolders( fileFoldObj.toString(), destArray );
      }
   }
   return destArray;
}

/*
function GetFileName(fullPath)
{
    var m = fullPath.match(/(.*)[\/\\]([^\/\\]+)\.\w+$/);
    return m[2];
}


function zeroPad(n, s) { 
   n = n.toString(); 
   while (n.length < s)  n = '0' + n; 
   return n; 
};
*/

function TrimFileName(fileName) { 
	var trimedFileName = fileName.substring(0, fileName.lastIndexOf(".")); 
	
	return trimedFileName;
};


function SaveForWeb(saveFile,jpegQuality) {
var sfwOptions = new ExportOptionsSaveForWeb(); 
   sfwOptions.format = SaveDocumentType.JPEG; 
   sfwOptions.includeProfile = false; 
   sfwOptions.interlaced = 0; 
   sfwOptions.optimized = true; 
   sfwOptions.quality = jpegQuality; //0-100 
activeDocument.exportDocument(saveFile, ExportType.SAVEFORWEB, sfwOptions);
}