def principled_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture):
    # import a principled shader with diffuse, roughness and normal nodes. 
    # Outputs the path to the material library level shader with principled_surface_importer.shader_node

    # example script
    # matname = hou.ui.readInput("Material Name")
    # matname = matname[1]
    # selectednode = hou.ui.selectNode()
    # importtextures = hou.ui.displayConfirmation("Import textures?")

    # if importtextures==True:
    #     diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
    #     roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
    #     normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
    # elif importtextures==False:
    #     diffuse_texture = ""
    #     roughness_texture = ""
    #     normal_texture = ""

    # jw_solaris_utils.principled_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)

    import hou

    matlib_node = hou.node(selectednode)

    # create nodes
    shader_node = matlib_node.createNode("principledshader::2.0", "principledshader_" + matname)
    
    # set parameters
    shader_node.parm("basecolorr").set(1)
    shader_node.parm("basecolorg").set(1)
    shader_node.parm("basecolorb").set(1)

    shader_node.parm("basecolor_useTexture").set(1)
    shader_node.parm("rough_useTexture").set(1)
    shader_node.parm("baseBumpAndNormal_enable").set(1)
    shader_node.parm("basecolor_texture").set(diffuse_texture)
    shader_node.parm("rough_texture").set(roughness_texture)
    shader_node.parm("baseNormal_texture").set(normal_texture)

    matlib_node.layoutChildren()

    principled_surface_importer.shader_node = shader_node

def arnold_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture):
    # import a Arnold standard surface with diffuse, roughness and normal nodes.
    # Outputs the path to the material library level shader with arnold_surface_importer.shader_node

    # example script
    # matname = hou.ui.readInput("Material Name")
    # matname = matname[1]
    # selectednode = hou.ui.selectNode()
    # importtextures = hou.ui.displayConfirmation("Import textures?")

    # if importtextures==True:
    #     diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
    #     roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
    #     normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
    # elif importtextures==False:
    #     diffuse_texture = ""
    #     roughness_texture = ""
    #     normal_texture = ""

    # jw_solaris_utils.arnold_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)

    import hou

    matlib_node = hou.node(selectednode)

    # create nodes
    matbuilder_node = matlib_node.createNode("arnold_materialbuilder", "arnold_materialbuilder_" + matname)
    arnoldsurface_node = matbuilder_node.createNode("arnold::standard_surface", "standard_surface_" + matname)
    diffuse_node = matbuilder_node.createNode("arnold::image", "image_diffuse_" + matname)
    roughness_node = matbuilder_node.createNode("arnold::image", "image_roughness_" + matname)
    normal_node = matbuilder_node.createNode("arnold::image", "image_normal_" + matname)
    normalmap_node = matbuilder_node.createNode("arnold::normal_map", "normal_map_" + matname)

    # connect nodes
    arnoldsurface_node.setInput(1, diffuse_node, 0)
    arnoldsurface_node.setInput(6, roughness_node, 1)
    arnoldsurface_node.setInput(39, normalmap_node, 0)
    normalmap_node.setInput(0, normal_node, 0)
    matbuilder_path = matbuilder_node.path()
    hou.node(matbuilder_path + "/OUT_material").setInput(0, arnoldsurface_node, 0)
    
    # set parameters
    diffuse_node.parm("filename").set(diffuse_texture)
    roughness_node.parm("filename").set(roughness_texture)
    normal_node.parm("filename").set(normal_texture)

    matbuilder_node.layoutChildren()

    arnold_surface_importer.shader_node = matbuilder_node

def usd_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture):
    # import a USD preview surface with diffuse and roughness nodes.
    # Outputs the path to the material library level shader with usd_surface_importer.shader_node

    # example script
    # matname = hou.ui.readInput("Material Name")
    # selectednode = hou.ui.selectNode()
    # importtextures = hou.ui.displayConfirmation("Import textures?")

    # if importtextures==True:
    #     diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
    #     roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
    #     normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
    # elif importtextures==False:
    #     diffuse_texture = ""
    #     roughness_texture = ""
    #     normal_texture = ""

    # jw_solaris_utils.usd_surface_importer(selectednode, matname[1], diffuse_texture, roughness_texture, normal_texture)
    
    import hou

    matlib_node = hou.node(selectednode)
    ## create nodes
    usdsurf_node = matlib_node.createNode("usdpreviewsurface", "usdpreviewsurface_" + matname)
    diffuse_node = matlib_node.createNode("usduvtexture::2.0", "usduvtexture_diffuse_" + matname)
    roughness_node = matlib_node.createNode("usduvtexture::2.0", "usduvtexture_roughness_" + matname)
    normal_node = matlib_node.createNode("usduvtexture::2.0", "usduvtexture_normal_" + matname)
    ## connect nodes
    usdsurf_node.setInput(0, diffuse_node, 4)
    usdsurf_node.setInput(5, roughness_node, 0)
    usdsurf_node.setInput(11, normal_node, 0)
    ## set parameters
    diffuse_node.parm("sourceColorSpace").set("sRGB")
    roughness_node.parm("sourceColorSpace").set("raw")
    normal_node.parm("sourceColorSpace").set("raw")
    diffuse_node.parm("file").set(diffuse_texture)
    roughness_node.parm("file").set(roughness_texture)
    normal_node.parm("file").set(normal_texture)

    matlib_node.layoutChildren()

    usd_surface_importer.shader_node = usdsurf_node

def pxr_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture):
    # import a pixar standard surface with diffuse, roughness and normal nodes.
    # Outputs the path to the material library level shader with pxr_surface_importer.shader_node

    # example script
    # matname = hou.ui.readInput("Material Name")
    # selectednode = hou.ui.selectNode()
    # importtextures = hou.ui.displayConfirmation("Import textures?")

    # if importtextures==True:
    #     diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
    #     roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
    #     normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
    # elif importtextures==False:
    #     diffuse_texture = ""
    #     roughness_texture = ""
    #     normal_texture = ""

    # jw_solaris_u tils.pxr_surface_importer(selectednode, matname[1], diffuse_texture, roughness_texture, normal_texture)

    import hou

    matlib_node = hou.node(selectednode)
    ## create nodes
    pxrsrf_node = matlib_node.createNode("pxrsurface::3.0", "pxrsurface_" + matname)
    diffuse_node = matlib_node.createNode("pxrtexture::3.0", "pxrtexture_diffuse_" + matname)
    roughness_node = matlib_node.createNode("pxrtexture::3.0", "pxrtexture_roughness_" + matname)
    normal_node = matlib_node.createNode("pxrnormalmap::3.0", "pxrtexture_normal_" + matname)

    ## connect nodes
    pxrsrf_node.setInput(2, diffuse_node, 0)
    pxrsrf_node.setInput(14, roughness_node, 1)
    pxrsrf_node.setInput(100, normal_node, 0)
    
    ## set parameters
    pxrsrf_node.parm("specularFresnelMode").set(1)
    diffuse_node.parm("filename").set(diffuse_texture)
    roughness_node.parm("filename").set(roughness_texture)
    normal_node.parm("filename").set(normal_texture)

    matlib_node.layoutChildren()

    pxr_surface_importer.shader_node = pxrsrf_node

def mtlx_surface_importer(selectednode, matname,  diffuse_texture, roughness_texture, normal_texture):
    # import a materialX standard surface with diffuse, roughness and normal nodes.
    # Outputs the path to the material library level shader with mtlx_surface_importer.shader_node

    # example script
    # matname = hou.ui.readInput("Material Name")
    # matname = matname[1]
    # selectednode = hou.ui.selectNode()
    # importtextures = hou.ui.displayConfirmation("Import textures?")

    # if importtextures==True:
    #     diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
    #     roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
    #     normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
    # elif importtextures==False:
    #     diffuse_texture = ""
    #     roughness_texture = ""
    #     normal_texture = ""
        
    # jw_solaris_utils.mtlx_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)

    import hou

    matlib_node = hou.node(selectednode)
    ## create nodes
    mtlxstandsurf_node = matlib_node.createNode("mtlxstandard_surface", "mtlxstandard_surface_" + matname)
    mtlxtexcoord_node = matlib_node.createNode("mtlxtexcoord", "mtlxtexcoord_" + matname)
    mtlxdiff_node = matlib_node.createNode("mtlximage", "mtlximage_diffuse_" + matname)
    mtlxrough_node = matlib_node.createNode("mtlximage", "mtlximage_roughness_" + matname)
    mtlxnrml_node = matlib_node.createNode("mtlximage", "mtlximage_normal_" + matname)
    mtlxnrmlmap_node = matlib_node.createNode("mtlxnormalmap", "mtlxnormalmap_" + matname)
    
    ## connect nodes
    mtlxstandsurf_node.setInput(1, mtlxdiff_node, 0)
    mtlxstandsurf_node.setInput(6, mtlxrough_node, 0)
    mtlxstandsurf_node.setInput(40, mtlxnrmlmap_node, 0)
    mtlxnrmlmap_node.setInput(0, mtlxnrml_node, 0)
    mtlxnrml_node.setInput(1, mtlxtexcoord_node, 0)
    mtlxdiff_node.setInput(1, mtlxtexcoord_node, 0)
    mtlxrough_node.setInput(1, mtlxtexcoord_node, 0)
    matlib_node.layoutChildren()
    
    ## set parameters
    mtlxtexcoord_node.parm('signature').set('vector2')
    mtlxdiff_node.parm('filecolorspace').set('srgb_texture')
    mtlxrough_node.parm('filecolorspace').set('srgb_texture')
    mtlxnrml_node.parm('filecolorspace').set('srgb_texture')
    mtlxrough_node.parm('signature').set('float')
    mtlxnrml_node.parm('signature').set('vector3')
    
    mtlxdiff_node.parm('file').set(diffuse_texture)
    mtlxrough_node.parm('file').set(roughness_texture)
    mtlxnrml_node.parm('file').set(normal_texture)

    mtlx_surface_importer.shader_node = mtlxstandsurf_node

def split_to_components(infile, removeprefix, generatematerials, diffuse_texture, roughness_texture, normal_texture, uvtransform, uvunwrap):    
    # takes in a geometry file and splits it into usd comonents based on the 'name' attribute, you can choose to append
    # uvtransform and unwrap sops as well as create basic materials. This was created to import BIM files and split them
    # into their relative components.
    
    # example script

    # infile = hou.ui.selectFile(title="File to split into components")
    # removeprefix = hou.ui.readInput(message="Prefix to remove from name attribute")
    # uvtransform = hou.ui.displayConfirmation(text="Do you want to append a UV Transform SOP to each component?")
    # uvunwrap = hou.ui.displayConfirmation(text="Do you want to append a UV Unwrap SOP to each component?")
    # generatematerials = hou.ui.displayConfirmation(text="Do you want to generate materials for each component?")
    # importtextures = hou.ui.displayConfirmation("Import textures?")

    # if importtextures==True:
    #     diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
    #     roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
    #     normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
    # elif importtextures==False:
    #     diffuse_texture = ""
    #     roughness_texture = ""
    #     normal_texture = ""

    # jw_solaris_utils.split_to_components(infile, removeprefix[1], generatematerials, diffuse_texture, roughness_texture, normal_texture, uvtransform, uvunwrap)
        
    import re 
    import hou 

    stage = hou.node('/stage') 
    ## import file in sopnet
    sopnet_node = stage.createNode('sopnet', "objectimport")
    file_node = sopnet_node.createNode('file')
    file_node.parm('file').set(infile)

    ## rescale
    transform_node = sopnet_node.createNode("xform", "rescale")
    matchsize_node = sopnet_node.createNode("matchsize")
    transform_node.setInput(0, file_node, 0)
    matchsize_node.setInput(0, transform_node, 0)
    transform_node.parm("scale").set(.01)
    matchsize_node.parm("justify_y").set("min")

    ## remove prefix 
    name_node = sopnet_node.createNode('name')
    name_node.setInput(0, matchsize_node, 0)
    name_node.parm('numnames').set(0)
    name_node.parm('numrenames').set(1)
    name_node.parm('from1').set(removeprefix + "*")
    name_node.parm('to1').set("*")

    ## create output null
    null_node = sopnet_node.createNode('null', 'OUT')
    null_node.setInput(0, name_node, 0)
    sopnet_node.layoutChildren()

    ## get name attrib from file
    filegeo = null_node.geometry()
    name_attribs = filegeo.findPrimAttrib('name').strings()

    if generatematerials == True:
        # ask for material types
        mattypes = hou.ui.selectFromList(["materialX","Principled", "Arnold", "usdPreview"], message="Material types to generator:", clear_on_cancel=True)

    ## create component builder for each name
    for name in name_attribs:

        ## turn name variable into houdini compatible node names, someone please fix this
        nodename = re.sub("[^0-9a-zA-Z\.]+", "_", name)
        nodename = re.sub("\.+", "_", nodename)

        ## create component geo
        geo_node = stage.createNode('componentgeometry')
        geosubpath = geo_node.path() ## component geo uses subnetsworks this gets that node
        geosub_node = hou.node(geosubpath + "/sopnet/geo")
        objmerge_node = geosub_node.createNode('object_merge')
        objmerge_node.parm('objpath1').set(null_node.path())
        suboutput_node = hou.node(geosubpath + "/sopnet/geo/default")
        
        ## delete extra geometry
        delextra_node = geosub_node.createNode('blast')
        delextra_node.parm('group').set("@name=" + '"' + name + '"')
        delextra_node.parm('negate').set(1)
        
        ## delete attributes and groups
        attribdelete_node = geosub_node.createNode('attribdelete')
        groupdelete_node = geosub_node.createNode('groupdelete')
        attribdelete_node.parm('negate').set(1)
        attribdelete_node.parm('ptdel').set("P")
        attribdelete_node.parm('vtxdel').set("N uv")
        groupdelete_node.parm('group1').set("*")
        
        ## set geo node inputs
        delextra_node.setInput(0, objmerge_node, 0)
        attribdelete_node.setInput(0, delextra_node, 0)
        groupdelete_node.setInput(0, attribdelete_node, 0)
        suboutput_node.setInput(0, groupdelete_node, 0)
        
        ## create component material
        matlib_node = stage.createNode('materiallibrary')
        matlib_node.parm('matpathprefix').set('/ASSET/mtl/')
        
        ## component output nodes
        assignmat_node = stage.createNode('componentmaterial')
        componentoutput_node = stage.createNode('componentoutput', nodename)
        assignmat_node.setInput(0, geo_node, 0)
        assignmat_node.setInput(1, matlib_node, 0)
        componentoutput_node.setInput(0, assignmat_node, 0)
      
        stage.layoutChildren()

        ## Create UV Transform Nodes
        if (uvtransform==True) and (uvunwrap==True):
            uvtrans_node = geosub_node.createNode('uvtransform::2.0')
            uvunwrap_node = geosub_node.createNode('uvunwrap')
            uvunwrap_node.setInput(0, groupdelete_node, 0)
            uvtrans_node.setInput(0, uvunwrap_node, 0)
            suboutput_node.setInput(0, uvtrans_node, 0)

        elif (uvtransform==True) and (uvunwrap==False):
            uvtrans_node = geosub_node.createNode('uvtransform::2.0')   
            uvtrans_node.setInput(0, groupdelete_node, 0)
            suboutput_node.setInput(0, uvtrans_node, 0)

        elif (uvtransform==True) and (uvunwrap==False):
            uvunwrap_node = geosub_node.createNode('uvunwrap')   
            uvunwrap_node.setInput(0, groupdelete_node, 0)
            suboutput_node.setInput(0, uvunwrap_node, 0)   

        geosub_node.layoutChildren()
        
        ## autogenerate materials
        if generatematerials==True:  
            
            matname = nodename

            ## returns the node path for the material library
            selectednode = hou.Node.path(matlib_node)

            collect_node = matlib_node.createNode("collect", matname)
                       
            for x in mattypes:

                if x == 0:
                    usd_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)  
                    nodepath = usd_surface_importer.shader_node.path()
                    usdshader_node = hou.node(nodepath)
                    usdshader_node.setMaterialFlag(False)
                    collect_node.setNextInput(usdshader_node, 0)

                elif x == 1:
                    mtlx_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)  
                    nodepath = mtlx_surface_importer.shader_node.path()
                    mtlxshader_node = hou.node(nodepath)
                    mtlxshader_node.setMaterialFlag(False)
                    collect_node.setNextInput(mtlxshader_node, 0)
                    
                elif x == 2:
                    principled_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)
                    nodepath = principled_surface_importer.shader_node.path()
                    principledshader_node = hou.node(nodepath)
                    principledshader_node.setMaterialFlag(False)
                    collect_node.setNextInput(principledshader_node, 0)
                    
                elif x == 3:
                    arnold_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)
                    nodepath = arnold_surface_importer.shader_node.path()
                    arnoldshader_node = hou.node(nodepath)
                    arnoldshader_node.setMaterialFlag(False)
                    collect_node.setNextInput(arnoldshader_node, 0)       

            matlib_node.layoutChildren()

def import_component_library(directory):
    ## looks at a directory and filters throuhg all subdirectories for .usd files to import via reference LOPS.

    ## example script
    ## jw_solaris_utils.import_component_library(directory)

    import os
    import hou

    rootdir = directory
    extension = ".usd"
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(extension):
                stage = hou.node("/stage")
                usdpath = os.path.join(subdir, file)
                filename = os.path.splitext(file)
                reference_node = stage.createNode("reference", filename[0])
                reference_node.parm("filepath1").set(usdpath)

                stage.layoutChildren()
                # print(os.path.join(subdir, file))
            else:
                continue

def universal_material_import(selectednode, matname, diffuse_texture, roughness_texture, normal_texture):
    # importes multiple render shaders into a collect node for use in component creation

    # example script
    # matname = hou.ui.readInput("Material Name")
    # matname = matname[1]
    # selectednode = hou.ui.selectNode()
    # importtextures = hou.ui.displayConfirmation("Import textures?")

    # if importtextures==True:
    #     diffuse_texture = hou.ui.selectFile(title='Diffuse Texture For ' + matname)
    #     roughness_texture = hou.ui.selectFile(title='Roughness Texture For ' + matname)
    #     normal_texture = hou.ui.selectFile(title='Normal Texture For ' + matname)
    # elif importtextures==False:
    #     diffuse_texture = ""
    #     roughness_texture = ""
    #     normal_texture = ""

    # jw_solaris_utils.universal_material_import(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)

    import hou

    mattypes = hou.ui.selectFromList(["usdPreview", "materialX","Principled", "Arnold"], message="Material types to generator:", clear_on_cancel=True)

    matlib_node = hou.node(selectednode)
    matlib_path = matlib_node.path()
    collect_node = matlib_node.createNode("collect", matname)

    for x in mattypes:

        if x == 0:
            usd_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)  
            nodepath = usd_surface_importer.shader_node.path()
            usdshader_node = hou.node(nodepath)
            usdshader_node.setMaterialFlag(False)
            collect_node.setNextInput(usdshader_node, 0)

        elif x == 1:
            mtlx_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)  
            nodepath = mtlx_surface_importer.shader_node.path()
            mtlxshader_node = hou.node(nodepath)
            mtlxshader_node.setMaterialFlag(False)
            collect_node.setNextInput(mtlxshader_node, 0)
            
        elif x == 2:
            principled_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)
            nodepath = principled_surface_importer.shader_node.path()
            principledshader_node = hou.node(nodepath)
            principledshader_node.setMaterialFlag(False)
            collect_node.setNextInput(principledshader_node, 0)
            
        elif x == 3:
            arnold_surface_importer(selectednode, matname, diffuse_texture, roughness_texture, normal_texture)
            nodepath = arnold_surface_importer.shader_node.path()
            arnoldshader_node = hou.node(nodepath)
            arnoldshader_node.setMaterialFlag(False)
            collect_node.setNextInput(arnoldshader_node, 0)
        
        matlib_node.layoutChildren()

            

       
        