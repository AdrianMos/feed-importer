// Script version: V3.0, 07.01.2018
main();

function main() {
    
    var inFolder = Folder(scriptPath() + '/mari neprocesate')
    if(inFolder == null) {
        alert("Input folder nok!");
        return;
    }
        
    var outFolder = Folder(scriptPath() + '/procesate');
    if(outFolder == null) {
        alert("Output folder nok!");
        return;
    }
    
    var folders = [];
    folders = getSubfolders(inFolder, folders);
    folders.unshift(inFolder); // add top folder to array
    
    for(var f in folders) {
       var files = folders[f].getFiles(/.+\.(?:jpg|jpe?g|[ew]mf|eps|tiff?|bmp|png)$/i)
       
       for(var j in files) {
            try {
                open(files[j]);
                doc = app.activeDocument; 
                doc.changeMode(ChangeMode.RGB); 
                
                if ((doc.width>doc.height) && (doc.width>UnitValue(800,"px")))
                    doc.resizeImage(UnitValue(800,"px"),null,null,ResampleMethod.BICUBIC);
                else if ((doc.width<doc.height) && (doc.height>UnitValue(800,"px")))
                    doc.resizeImage(null,UnitValue(600,"px"),null,ResampleMethod.BICUBIC);
               
                var imageQuality = 60;
                var outFilename = generateFilePath(outFolder, files[j]);

                var resizedFile = new File(outFilename);
                saveForWeb(resizedFile, imageQuality);
                app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);             
            }
            catch(err) {
              
                copyFileToErrorFolder(files[j]);        
                alert("Eroare imagine: " + files[j].displayName + 
                      ". Imaginea a fost copiata in folderul /erori imagini mari/. Trebuie prelucrata manual !");  
            }
        }
    }
    
    alert("Procesare finalizata !");  
}

function copyFileToErrorFolder(file) {
    var errorFolder = Folder(scriptPath() + '/erori/erori imagini mari');
    file.copy(decodeURI(errorFolder) + "/" + file.displayName)       
}


function generateFilePath(folder, file) {
  
    //var extension = file.name.substring(file.name.lastIndexOf("."), file.name.length);
    //var fileNameNoExtension = file.name.substring(0, file.name.lastIndexOf("."));
    return folder + "/" + file.name;
};


function scriptPath() {
    var currentScript = new File($.fileName);  
    return currentScript.path;
}    

function isFolder(item) {
    return !(item instanceof File)
}

function getSubfolders(path, outArray) {
    var items = Folder(path).getFiles();
    
    for (var i = 0; i<items.length; i++) {
        if (isFolder(items[i])) {         
            outArray.push(Folder(items[i]));
            getSubfolders(items[i].toString(), outArray);
        }
   }
   return outArray;
}


function saveForWeb(resizedFile, imageQuality) {
    var options = new ExportOptionsSaveForWeb(); 
    options.format = SaveDocumentType.JPEG; 
    options.quality = imageQuality; //0-100 
    options.includeProfile = false; 
    options.interlaced = 0; 
    options.optimized = true; 
    activeDocument.exportDocument(resizedFile, ExportType.SAVEFORWEB, options);
}