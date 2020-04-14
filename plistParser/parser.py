import plistlib
import sys
from lxml import etree
import os

def readDictionary(dict_name):
    colors = {}
    strings = {}
    lists = {}
    with open(dict_name, 'rb') as fp:
        plist = plistlib.load(fp)
        print(plist)
        for key in plist.keys():
            # print(key)
            value = plist[key]
            if isinstance(plist[key], str):
                if value.startswith("0x"):
                    value = eval(value)
                    colors[key] = value
                else:
                    strings[key] = value
                # endif
            elif isinstance(plist[key], list):
                lists[key] = value
            # endif
        # endfor
    # endwith
    print(colors)
    print(strings)
    print(lists)
    return colors, strings, lists


def write_resource(resources_dict, filename, xml_resource_type, is_hex_string=False):
    root = etree.Element("resources")
    if len(colors) > 0:
        colorsPath = os.path.join(path, filename)
        # if not os.path.exists(colorsPath):
        #     os.mkdir(colorsPath)
        # # endif
        index = 1
        for resource in resources_dict:
            subelement = etree.SubElement(root, xml_resource_type)
            subelement.set("name", resource)
            if is_hex_string:
                print(resources_dict[resource])
                subelement.text = str(hex(resources_dict[resource])).replace("0x", "#")
            else:
                subelement.text = str(resources_dict[resource])
            # endif
            index += 1
        # endfor
        etree.dump(root)
        with open(colorsPath, 'w') as fp:
            xml_file_header = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
            fp.writelines([xml_file_header])
            fp.write(xml_file_header)
            fp.write(etree.tostring(root, encoding='unicode', pretty_print=True))
        # endwith
    # endif


def parse_file(plistName):
    global colors, path
    colors, strings, lists = readDictionary(plistName)
    print(os.getcwd())
    path = os.path.join(os.getcwd(), plistName.replace(".plist", ""))
    if not os.path.exists(path):
        os.mkdir(path)
    # endif
    path = os.path.join(path, "res")
    if not os.path.exists(path):
        os.mkdir(path)
    # endif
    path = os.path.join(path, "values")
    if not os.path.exists(path):
        os.mkdir(path)
    # endif
    write_resource(colors, "colors.xml", "color", is_hex_string=True)
    write_resource(strings, "strings.xml", "string")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        plistName = sys.argv[1]
        parse_file(plistName)
    else:
        for file in os.listdir(os.getcwd()):
            if file.endswith(".plist"):
                parse_file(file)
            # endif
            print(file)
        # endfor
        print("Not enough arguments received: {0}".format(sys.argv))
    # endif
