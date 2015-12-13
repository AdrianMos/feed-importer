// Script version: V2.1   
   main();
function main(){
var max;
var folders =[];
//var topLevel = Folder.selectDialog("Please select top level folder");   
var topLevel = Folder('C:/haiducel importuri/_ imagini noi/mari neprocesate')
if(topLevel == null ) return;
//var outPutFolder = Folder.selectDialog("Please select output folder");
var outPutFolder = Folder('C:/haiducel importuri/_ imagini noi/procesate')
if(outPutFolder == null ) return;
//get a list of all sub folders
folders = FindAllFolders(topLevel, folders);
//add selected foler
folders.unshift(topLevel);
// set up a counter
var Counter = 1;
//iterate through the folder list
for(var f in folders){
   var fileList = folders[f].getFiles(/.+\.(?:jpg|jpe?g|[ew]mf|eps|tiff?|bmp|png)$/i)
   for(var j in fileList){
       open(fileList[j]);
// get a reference to the current (active) document and store it in a variable named "doc"
doc = app.activeDocument; 
// change the color mode to RGB. Important for resizing GIFs with indexed colors, to get better results
doc.changeMode(ChangeMode.RGB); 
// these are our values for the end result width and height (in pixels) of our image


if ((doc.width>doc.height) && (doc.width>UnitValue(800,"px")))
	doc.resizeImage(UnitValue(800,"px"),null,null,ResampleMethod.BICUBIC);
else if ((doc.width<doc.height) && (doc.height>UnitValue(800,"px")))
	doc.resizeImage(null,UnitValue(600,"px"),null,ResampleMethod.BICUBIC);
	
var fileExtension = fileList[j].name.substring(fileList[j].name.lastIndexOf("."), fileList[j].name.length)
var saveFile = new File(outPutFolder+"/"+TrimFileName(fileList[j].name)+fileExtension);



//Save document
SaveForWeb(saveFile,60);
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