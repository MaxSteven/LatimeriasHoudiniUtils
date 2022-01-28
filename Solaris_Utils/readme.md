# Josh Weber Solaris Utils

This module is meant to speed up workflows in Solaris particularly in the ArchVIZ industry.

Currently symlinked into the `python3.7libs` directory as the PYTHONPATH environment variable returns errors.

---

# Table of Functions:
- [mtlxUsdImporter](#mtlxUsdImporter)
- [splitToComponents](#splitToComponents)

---

## mtlxUsdImporter

mtlxUsdImporter(selectednode, matname, importtextures)

This creates a material network using USD preview surfaces for viewport and materialX nodes for render materials. 

***selectednode***         
The material library nodes for the material network to be created in. This reads a single string which can be obtained through the `hou.ui.selectNode` function.

***matname***   
This is the name of the material which will be appended to each node in the material network. Takes a string input that must be a valid node name. To validate names you can use `re.sub("[^0-9a-zA-Z\.]+", "_", name)`. To obtain names you can use `hou.ui.readInput()` which will return a tuple which you can take the [1] index of to get the string name. 

***importtextures***    
This takes a boolean value. This can be obtained through the `hou.ui.displayConfirmation()` function. If True then the function will run `hou.ui.selectFile()` and have the user choose files for diffuse, roughness and normal. 


#### Example Shelf Tool
```
import jw_solaris_utils

selectednode = hou.ui.selectNode(title="Material Library to Create Material In")
matname = hou.ui.readInput(message="Material Name")
importtextures = hou.ui.displayConfirmation(text="Import Textures?")
print(matname[1])
print(selectednode)
print(importtextures)

jw_solaris_utils.mtlxUsdImporter(selectednode, matname[1], importtextures)
```
---

## splitToComponents

splitToComponents(infile, removeprefix, generate_materials, importtextures, uvtransform, uvunwrap):

This splits the selected file into multiple components based on the unique name attribute values. Used for imported BIM files for quick procedural process visualization in Solaris. 

Dependencies: re

***infile***             
This takes a string input for the absolute path to the file being imported. This can be obtained using `hou.ui.selectFile()`.

***removeprefix***            
This removes a prefix from the name attribute on the imported geometry, sometimes this happens when import files from BIM or CAD softwares and cna be used to simplify component/material names. For example if your name attribute has values like `my_architecture_project/Foundation` you would set `removeprefix = "my_architecture_project/" to return 'foundation'.

***generatematerials***                     
This takes a boolean value. This can be obtained through the `hou.ui.displayConfirmation()` function. If True every component will get a generate a single materialX based network using the mtlxUsdImporter function with the material name set to the component name. 

***importtextures***            
TThis takes a boolean value. This can be obtained through the `hou.ui.displayConfirmation()` function. If True then the function will run `hou.ui.selectFile()` and have the user choose files for diffuse, roughness and normal. ***Warning*** this will ask for textures for every component in your project which can add up quickly.

***uvtransform***           
TThis takes a boolean value. This can be obtained through the `hou.ui.displayConfirmation()` function. If True a uvtransform SOP will be appended to the end of each component geometry.

***uvunwrap***            
TThis takes a boolean value. This can be obtained through the `hou.ui.displayConfirmation()` function. If True a uvunwrap SOP will be appended to the end of each component geometry.

#### Example Shelf Tool
```
import jw_solaris_utils

infile = hou.ui.selectFile(title="File to split into components")
removeprefix = hou.ui.readInput(message="Prefix to remove from name attribute")
generatematerials = hou.ui.displayConfirmation(text="Do you want to generate materials for each component?")
importtextures = hou.ui.displayConfirmation(text="Do you want to import textures now? Warning! This will make you select textures for each material")
uvtransform = hou.ui.displayConfirmation(text="Do you want to append a UV Transform SOP to each component?")
uvunwrap = hou.ui.displayConfirmation(text="Do you want to append a UV Unwrap SOP to each component?")

jw_solaris_utils.splitToComponents(infile, removeprefix[1], generatematerials, importtextures, uvtransform, uvunwrap)
```
---
