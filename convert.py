import xml.etree.ElementTree as xml
import json
import cv2

#load json file
with open('example.json') as json_file:
	json_data = json.load(json_file)

#declare file/folder names and paths
working_dir = 'any_dir'
fixed_path = '/yourpath/' + working_dir + '/' #filename has to be appended as well. (will be appended from json file)
num_of_data = len(json_data)

#loop through every json object

for data_index in range(num_of_data):
    
    file_name = json_data[data_index]['name'] #get the name of the image file
    output_xml_filename = file_name[:-3] + '.xml' # output xml file name is the image file name without the extension
    file_path = fixed_path + file_name #full path of the image
    
    #XML file structure
    root = xml.Element("annotation") #root element

    #XML file structure
    #Get the information from the json data

    #folder data
    folder      = xml.SubElement(root, "folder")
    folder.text = working_dir

    #filename data
    filename      = xml.SubElement(root, "filename") #NOTE: this variable has no underscore, "_"
    filename.text = file_name
    
    #path data
    path      = xml.SubElement(root, "path")
    path.text = file_path
    
    #source data
    source_element = xml.Element("source")
    root.append(source_element)
    database       = xml.SubElement(source_element, "database")
    database.text  = "Unknown"
    
    
    #UNCOMMENT THESE 2 LINES ONLY IF YOUR JSON DATA HAS NO IMAGE HEIGHT AND WIDTH!
    #                           --START CODE--
    #the image has to be read first in order to get the details of the image size for the next xml node
    image = cv2.imread(file_path) #read the image
    img_height, img_width, img_depth = image.shape #get the image height, width and depth
    #                            --END CODE--
    
    #size data 
    size_element = xml.Element("size")
    root.append(size_element)
    width        = xml.SubElement(size_element, "width")
    height       = xml.SubElement(size_element, "height")
    depth        = xml.SubElement(size_element, "depth")
    width.text   = str(img_width)
    height.text  = str(img_height)
    depth.text   = str(img_depth)
    
    #segmented data
    segmented      = xml.SubElement(root, "segmented")
    segmented.text = "0"
    
    #object data
    objects = json_data[data_index]["labels"] #the list of objects
    unwanted_lists = ['traffic light', 'traffic sign', 'drivable area', 'lane'] #list of object categories to be ignored
    
    for obj_index in range(len(objects)): #loop through the objects
        
        object_category = objects[obj_index]['category'] #category of the object
        
        if object_category in unwanted_lists: #skip the loop if the category is in unwanted_lists
            continue
        
        obj_element = xml.Element("object") #create object node
        root.append(obj_element)
        
        #name data
        name      = xml.SubElement(obj_element, "name")
        name.text = object_category
        
        #pose data
        pose      = xml.SubElement(obj_element, "pose")
        pose.text = "Unspecified"
        
        #truncated data
        truncated      = xml.SubElement(obj_element, "truncated")
        truncated.text = "0" if objects[obj_index]['attributes']['truncated'] == False else "1" #binary format boolean
        
        #occluded data
        occluded      = xml.SubElement(obj_element, "occluded")
        occluded.text = "0" if objects[obj_index]['attributes']['occluded'] == False else "1" #binary format boolean
        
        #bounding box data
        bounding_box_element = xml.Element("bndbox")
        obj_element.append(bounding_box_element)
        xmin      = xml.SubElement(bounding_box_element, "xmin")        
        ymin      = xml.SubElement(bounding_box_element, "ymin")
        xmax      = xml.SubElement(bounding_box_element, "xmax")
        ymax      = xml.SubElement(bounding_box_element, "ymax")
        xmin.text = objects[obj_index]['box2d']['x1']
        ymin.text = objects[obj_index]['box2d']['y1']
        xmax.text = objects[obj_index]['box2d']['x2']
        ymax.text = objects[obj_index]['box2d']['y2']
        
        
        

    #create XML tree and write the output
    tree = xml.ElementTree(root)
    with open(output_xml_filename, 'wb') as out:
        tree.write(out)