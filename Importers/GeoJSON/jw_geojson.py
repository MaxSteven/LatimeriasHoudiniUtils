# This code is called when instances of this SOP cook.
node = hou.pwd()
geo = node.geometry()


'''
This works by importing all attributes as string types, you can convert any attributes back to float or in with the below script
f@NEWATTRIB = atoi(s@ATTRIB);
Make new the new attribute you write has a new name otherwise it will return an error that you are trying to write type string
'''
# Add code to modify the contents of geo.
import json

path = node.evalParm("geojson_path")

with open(path, "r") as file:
    data = json.load(file)

features = data["features"]  
#get names and data types for attribs and initialize
first_item = features[0]
init_attribs = first_item["properties"]
init_shape = first_item["geometry"]
shapetype = init_shape["type"]
datatypes = []
for attrib in init_attribs:
#    if init_attribs[attrib] is None:
#        datatype = "none"
#    if isinstance(init_attribs[attrib], str) == True:
#         datatype = "empty"
#    if isinstance(init_attribs[attrib], float) == True:
#        datatype = 0.0
#    if isinstance(init_attribs[attrib], int) == True:
#        datatype = 0
    if shapetype == "Polygon" or "MultiPolygon":
        geo.addAttrib(hou.attribType.Prim, attrib, "")
    if shapetype == "Point":
        geo.addAttrib(hou.attribType.Point, attrib, "")
#    datatypes.append(datatype) 

#init bool attribute      
if shapetype == "Polygon" or "MultiPolygon":        
    geo.addAttrib(hou.attribType.Prim, "bool", 0)
    
for index, obj in enumerate(features):  
    shape = obj["geometry"]
    attribs = obj["properties"]  
    if shape is None: # pass null values
        continue
    
    if shape["type"] == "Point":
        ptpos = shape["coordinates"]
        ptpos.insert(1,0) #2d to 3d
        point = geo.createPoint()
        point.setPosition(ptpos)
        for attrib in attribs:
            point.setAttribValue(attrib, str(attribs[attrib]))
            
    if shape["type"] == "Polygon":
        poly = geo.createPolygon()
        ptpositions = shape["coordinates"]
        
        for ptpos in ptpositions[0]:
            ptpos.insert(1,0)
            point = geo.createPoint()
            point.setPosition(ptpos)
            poly.addVertex(point)
        for attrib in attribs: 
                poly.setAttribValue(attrib, str(attribs[attrib]))

    if shape["type"] == "LineString":
        poly = geo.createPolygon(is_closed=False)
        ptpositions = shape["coordinates"]
        for ptpos in ptpositions:
            ptpos.insert(1,0)
            point = geo.createPoint()
            point.setPosition(ptpos)
            poly.addVertex(point)
                    
        for i, attrib in enumerate(attribs):
            poly.setAttribValue(attrib, str(attribs[attrib]))
                
    if shape["type"] == "MultiLineString":
        polys = shape["coordinates"]
        for i in polys:
            poly = geo.createPolygon(is_closed=False)
            for ptpos in i:
                ptpos.insert(1,0)
                point = geo.createPoint()
                point.setPosition(ptpos)
                poly.addVertex(point)
        
            for i, attrib in enumerate(attribs):
                poly.setAttribValue(attrib, str(attribs[attrib]))    
        
    if shape["type"] == "MultiPolygon":
        polys = shape["coordinates"]
        for i in polys: # i = polygon
            poly = geo.createPolygon()
            if len(i) == 1:
                for j in i: # J is list of points positions
                    for ptpos in j: # loops through list of point positions in J 
                        ptpos.insert(1,0)
                        point = geo.createPoint()
                        point.setPosition(ptpos)
                        poly.addVertex(point)
                    
                for attrib in attribs:
                    poly.setAttribValue(attrib, str(attribs[attrib]))
                    
            # if poylgon has holes      
            if len(i) > 1: 
                for index, j in enumerate(i): # J is list of points positions
                    if index == 0: # extract first index as main polygon
                        for ptpos in j: # loops through list of point positions in J 
                            ptpos.insert(1,0)
                            point = geo.createPoint()
                            point.setPosition(ptpos)
                            poly.addVertex(point)
                    else: # create boolean polygons
                        boolpoly = geo.createPolygon()
                        for ptpos in j:
                            ptpos.insert(1,0)
                            point = geo.createPoint()
                            point.setPosition(ptpos)
                            boolpoly.addVertex(point)
                            boolpoly.setAttribValue("bool", 1)
                            
                for attrib in attribs:
                    poly.setAttribValue(attrib, str(attribs[attrib]))
    
    # if index > 13393:
    #     break

        