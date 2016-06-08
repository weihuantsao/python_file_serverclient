#!/usr/bin/python
# coding=UTF-8
import sys

workspace_path = '\\logdata\\'
read_data_file = 'log.txt'
workspace_path = sys.path[0] + workspace_path

# template(path_data,mark_template)
template = """<?xml version="1.0" encoding="UTF-8"?> 
<kml xmlns="http://www.opengis.net/kml/2.2"> 
    <Document> 
        <name>GPS Path</name> 
        <description>Path parsed from GPS data.</description> 
        <Style id="yellowLineGreenPoly"> 
            <LineStyle> 
                <color>7f00ffff</color> 
                <width>4</width> 
                <gx:labelvisibility>0</gx:labelvisibility> 
            </LineStyle> 
            <PolyStyle> 
                <color>7f00ff00</color> 
            </PolyStyle> 
        </Style> 

        <Placemark> 
            <name>Path</name> 
            <styleUrl>#yellowLineGreenPoly</styleUrl> 
            <LineString>  
                <tessellate>1</tessellate> 
                <coordinates>\n%s
                </coordinates>
            </LineString>
        </Placemark>%s
    </Document>
</kml>
"""

#mark_template(name , sensor_data , location)
mark_template = """
        <Placemark>
            <name>%s</name> 
            <description>\n%s
            </description>
            <styleUrl>#msn_ylw-pushpin</styleUrl>
            <Point>
                <coordinates>%s</coordinates>
            </Point>
        </Placemark>
"""

def FileCheck(fn):
    try:
      open(fn, "r")
      return 1
    except IOError:
      print "Error: File does not appear to exist."
      return 0

def File_Name_parser(line):
    try:
        data_element = line.split(" ")
        date = data_element[0].replace('-','')
        oclock = data_element[1].split(":")
        oclock = oclock[0]+'h'+oclock[1]+'m'
        file_name = date + '_' + oclock + '.kml'
        return file_name
    except:
        return 'noName.kml'

def usage():
    sys.stderr.write("USAGE: python txt2kml.py filename.txt")

try:
    read_data_file =  sys.argv[1]
except: 
        sys.stderr.write("ERROR: have no filename\n")
        usage()
        sys.exit(2)

if FileCheck(read_data_file):

    f = open (read_data_file,"r")  
    read_data= ""
    mark_point= "" 
    total_mark_point= ""
    total_latitude = ""
    total_name = ""
    total_description = ""

    while True:
        read_data = f.readline()
        if read_data == "":
            break
        elif read_data == "\n":
            continue
        data_element = read_data.split(",") 
        
        latitude = data_element[2] + "," + data_element[1] + "," + data_element[3]
        total_latitude = total_latitude + latitude + "\n"
        name = data_element[4]
        total_name = total_name + name + "\n"
        
  
        if data_element[5] == '\n':
            continue
        elif data_element[5] == '':    
            continue
        else:
            for k in range(len(data_element)): 
                if k >=5:
                    description = data_element[k]
                    total_description = total_description + description +"\n"     
                    mark_point =  mark_template % (name , total_description ,latitude)
            total_description = ""
        total_mark_point += mark_point
    f.close()
    
    f1 = open (workspace_path+File_Name_parser(total_name),"w")
    template = template % (total_latitude , total_mark_point)
    f1.write(template)
    f1.close()

    
