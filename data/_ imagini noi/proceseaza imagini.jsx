// Script version: V4.0, 10.01.2018
main();

function main() {
  
    var params_smallImages = { 
        inputFolder: '/mici neprocesate',
        outputFolder: '/procesate',
        brokenImagesFolder: '/erori/erori imagini mici/',
        imageQuality: 80,
        callback_generateFilename: generateSmallImageName,
        callback_processImage: resizeSmallImageAlgorithm
        };

    processImages(params_smallImages);


    var params_LargeImages = { 
        inputFolder: '/mari neprocesate',
        outputFolder: '/procesate',
        brokenImagesFolder: '/erori/erori imagini mari/',
        imageQuality: 60,
        callback_generateFilename: generateImageName,
        callback_processImage: resizeAlgorithm 
        };

    processImages(params_LargeImages)

    alert("Procesare finalizata !");
}




// SMALL IMAGES callbacks -------------------------------------------------------------
function generateSmallImageName(file) {   
  
    var extension = file.name.substring(file.name.lastIndexOf("."), file.name.length);
    var fileNameNoExtension = file.name.substring(0, file.name.lastIndexOf("."));
    
    return fileNameNoExtension + "_s" + extension;
}      
     
function resizeSmallImageAlgorithm() { 
    doc = app.activeDocument; 
    var max;
    if (doc.width>doc.height) {
        max = doc.width;
    }
    else {
        max = doc.height;
    }
    doc.resizeCanvas(max, max, AnchorPosition.MIDDLECENTER);
    doc.resizeImage(null,UnitValue(300,"px"),null,ResampleMethod.BICUBIC);
}

// LARGE IMAGES callbacks -------------------------------------------------------------
function generateImageName(file) {
    return file.name;
}

function resizeAlgorithm() {
    doc = app.activeDocument; 
    isLandscape = doc.width>doc.height

    if (isLandscape && (doc.width>UnitValue(800,"px")))
        doc.resizeImage(UnitValue(800,"px"),null,null,ResampleMethod.BICUBIC);
    else if (!isLandscape && (doc.height>UnitValue(800,"px")))
        doc.resizeImage(null,UnitValue(600,"px"),null,ResampleMethod.BICUBIC);     
}
//-------------------------------------------------------------------------------------


function processImages(config) {
    
    var inFolder = Folder(scriptPath() + config.inputFolder)
    if(inFolder == null) {
        alert("Input folder nok!");
        return;
    }
        
    var outFolder = Folder(scriptPath() + config.outputFolder);
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
                setBackgroundColor(255,255,255);
                
                config.callback_processImage();
                
                var outFilename = outFolder + "/" + config.callback_generateFilename(files[j]);
                
                var resizedFile = new File(outFilename);
                saveForWeb(resizedFile, config.imageQuality);
                app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);             
            }
            catch(err) {
                copyFileToErrorFolder(files[j],  config.brokenImagesFolder); 
                showBrokenImageMessage(files[j], config.brokenImagesFolder);             
            }
        }
    }  
}

// HELPERS -----------------------------------------------------------------------------
function scriptPath() {
    var currentScript = new File($.fileName);  
    return currentScript.path;
}  

function setBackgroundColor(r,g,b) {
    var color = app.backgroundColor;
    color.rgb.red = r;
    color.rgb.green = g;
    color.rgb.blue = b;
    app.backgroundColor = color;
 }
  
function showBrokenImageMessage(file, folder) {
    alert("Eroare imagine: " + file.displayName + 
          ". Imaginea a fost copiata in folderul " + 
          folder +
          ". Trebuie prelucrata manual !");
}        

function copyFileToErrorFolder(file, folder) {
    var errorFolder = Folder(scriptPath() + folder);
    file.copy(decodeURI(errorFolder) + "/" + file.displayName)       
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