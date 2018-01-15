#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#from xml.etree.ElementTree import Element, SubElement, tostring
from lxml.etree import Element, SubElement, tostring,ElementTree
import pprint
from xml.dom.minidom import parseString

def generateAnnotation(objectName,location,filename,width,height,annotationdir):


  node_root = Element('annotation')

  node_folder = SubElement(node_root, 'folder')
  node_folder.text = 'VOC2012'


  node_filename = SubElement(node_root, 'filename')
  node_filename.text = filename

  node_size = SubElement(node_root, 'size')
  node_width = SubElement(node_size, 'width')
  node_width.text = width

  node_height = SubElement(node_size, 'height')
  node_height.text = height

  node_depth = SubElement(node_size, 'depth')
  node_depth.text = '3'

  node_object = SubElement(node_root, 'object')
  node_name = SubElement(node_object, 'name')
  node_name.text = objectName
  node_difficult = SubElement(node_object, 'difficult')
  node_difficult.text = '0'
  node_bndbox = SubElement(node_object, 'bndbox')
  node_xmin = SubElement(node_bndbox, 'xmin')
  node_xmin.text = str(location[0])
  node_ymin = SubElement(node_bndbox, 'ymin')
  node_ymin.text = str(location[1])
  node_xmax = SubElement(node_bndbox, 'xmax')
  node_xmax.text = str(location[2])
  node_ymax = SubElement(node_bndbox, 'ymax')
  node_ymax.text = str(location[3])

  xml = tostring(node_root, pretty_print=True)  #格式化显示，该换行的换行
  dom = parseString(xml)
  print xml


  #tree = ElementTree(node_root)
  #tree.write(annotationdir+'/'+filename[:-4]+'.xml',encoding='utf-8')
  filexml = open(annotationdir+'/'+filename[:-4]+'.xml','w')
  filexml.write(xml)
  filexml.close()
