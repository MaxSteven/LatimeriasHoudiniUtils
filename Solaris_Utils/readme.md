# Solaris Utils

This module is meant to speed up workflows in Solaris particularly in the ArchVIZ industry.

Currently symlinked into the `python3.7libs` directory as the PYTHONPATH environment variable returns errors.

---

# Table of Functions:
- [Individual Material Importers](#Individual_Material_Importers)
- [Universal Material Import](#Universal_Material_Import)
- [Split To Components](#split_To_Components)
- [Import Component Library](#Import_Component_Library)

---

# Individual_Material_Importers

### A series of standard surface/uber material importers all take the same arugemnts. The supported materials are: Arnold, materialX, USD, Principled, PXR.

args: (selectednode, matname,  diffuse_texture, roughness_texture, normal_texture)

- mtlx_surface_importer(args)

- principled_surface_importer(args)

- arnold_surface_importer(args)

- usd_surface_importer(args)

- pxr_surface_importer(args)

***selectednode***         
The material library nodes for the material network to be created in. This reads a single string which can be obtained through the `hou.ui.selectNode` function.

***matname***   
This is the name of the material which will be appended to each node in the material network. Takes a string input that must be a valid node name. To validate names you can use `re.sub("[^0-9a-zA-Z\.]+", "_", name)`. To obtain names you can use `hou.ui.readInput()` which will return a tuple which you can take the [1] index of to get the string name. 

***diffuse_texture, roughness_texture, normal_texture***    
takes a string referencing the path to each texture which can be obtained with hou.ui.selectFile() 

#### Example Script
```
matname = hou.ui.readInput("Material Name")
matname = matname[1]
selectednode = hou.ui.selectNode()
importtextures = hou.ui.displayConfirmation("Import textures?")

if importtextures==True:
    diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
    roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
    normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
elif importtextures==False:
    diffuse_texture = ""
    roughness_texture = ""
    normal_texture = ""
    
jw_solaris_utils.mtlx_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)
```
---

## Universal_Material_Import

universal_material_import(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)

Imports selected render specific materials defined above and pipes them into a collect node for use in creating usd assets for multiple render engines. 

***selectednode***         
The material library nodes for the material network to be created in. This reads a single string which can be obtained through the `hou.ui.selectNode` function.

***matname***   
This is the name of the material which will be appended to each node in the material network. Takes a string input that must be a valid node name. To validate names you can use `re.sub("[^0-9a-zA-Z\.]+", "_", name)`. To obtain names you can use `hou.ui.readInput()` which will return a tuple which you can take the [1] index of to get the string name. 

***diffuse_texture, roughness_texture, normal_texture***    
takes a string referencing the path to each texture which can be obtained with hou.ui.selectFile() 

#### Example Script
```
matname = hou.ui.readInput("Material Name")
matname = matname[1]
selectednode = hou.ui.selectNode()
importtextures = hou.ui.displayConfirmation("Import textures?")

if importtextures==True:
    diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
    roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
    normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
elif importtextures==False:
    diffuse_texture = ""
    roughness_texture = ""
    normal_texture = ""

jw_solaris_utils.universal_material_import(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)
```
---
## Split_To_Components

split_to_components(infile, removeprefix, generatematerials, diffuse_texture, roughness_texture, normal_texture, uvtransform, uvunwrap)

This splits the selected file into multiple components based on the unique name attribute values. Used for imported BIM files for quick procedural process visualization in Solaris. 

Dependencies: re

***infile***             
This takes a string input for the absolute path to the file being imported. This can be obtained using `hou.ui.selectFile()`.

***removeprefix***            
This removes a prefix from the name attribute on the imported geometry, sometimes this happens when import files from BIM or CAD softwares and cna be used to simplify component/material names. For example if your name attribute has values like `my_architecture_project/Foundation` you would set `removeprefix = "my_architecture_project/" to return 'foundation'.

***generatematerials***                     
This takes a boolean value. This can be obtained through the `hou.ui.displayConfirmation()` function. If True every component will get a generate a single materialX based network using the mtlxUsdImporter function with the material name set to the component name. 

***diffuse_texture, roughness_texture, normal_texture***    
takes a string referencing the path to each texture which can be obtained with hou.ui.selectFile() 

***uvtransform***           
TThis takes a boolean value. This can be obtained through the `hou.ui.displayConfirmation()` function. If True a uvtransform SOP will be appended to the end of each component geometry.

***uvunwrap***            
TThis takes a boolean value. This can be obtained through the `hou.ui.displayConfirmation()` function. If True a uvunwrap SOP will be appended to the end of each component geometry.

#### Example Shelf Tool
```
infile = hou.ui.selectFile(title="File to split into components")
removeprefix = hou.ui.readInput(message="Prefix to remove from name attribute")
uvtransform = hou.ui.displayConfirmation(text="Do you want to append a UV Transform SOP to each component?")
uvunwrap = hou.ui.displayConfirmation(text="Do you want to append a UV Unwrap SOP to each component?")
generatematerials = hou.ui.displayConfirmation(text="Do you want to generate materials for each component?")
importtextures = hou.ui.displayConfirmation("Import textures?")

if importtextures==True:
    diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
    roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
    normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
elif importtextures==False:
    diffuse_texture = ""
    roughness_texture = ""
    normal_texture = ""

jw_solaris_utils.split_to_components(infile, removeprefix[1], generatematerials, diffuse_texture, roughness_texture, normal_texture, uvtransform, uvunwrap)
```
---

## Import_Component_Library

import_component_library(directory)

This imports .usd via reference LOPS by looking through the folder in the given directory, for example if you write assets out using the component builder you can search through the 'usd' directory that contains folders that have their own usd asset in them. 

***directory***
Takes a string that goes to the file directory. Can be obtained with hou.ui.selectFile(file_type=hou.fileType.Directory)

#### Example Shelf Tool
```
jw_solaris_utils.import_component_library(directory
```
