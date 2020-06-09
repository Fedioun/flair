
import xml.etree.ElementTree as ET
import time
import json
import string
xml_out = "xml_out.txt"

xo = open(xml_out, "w", encoding="utf8")
json_file_path = "/home/nosmoth/Documents/Datasets/desfosses_omnipage_et_jsonSimon/desfosses sample/1962_T2_T_0722_with-tags.json"
file = open(json_file_path)
data = json.load(file)



def main():

    omnipage_file_path = "/home/nosmoth/Documents/Datasets/desfosses_omnipage_et_jsonSimon/desfosses omni/1962_T2_T_0722.xml"

    tree = ET.parse(omnipage_file_path)
    find_words(tree.getroot())




    mark = False



    json_out = "./json_out.txt"
    with open(json_out, "w", encoding="utf8") as jo:


        find_in_json("juillet", data["data"][0])





        exit()
        for rubric in data["data"][0]["children"]:
            if mark:
                jo.write(" -------------- RUBRIQUE ------------\n")
            print(rubric["type"], rubric.keys())

            if "title" in rubric:
                for s in tokenize(rubric["title"]):
                    jo.write(s + "\n")

            if "text-tags" in rubric:
                for t in rubric["text-tags"]:
                    for s in tokenize(t[0]):
                        jo.write(s + "\n")




            # Table-section or balance
            if "children" in rubric:
                for table in rubric["children"]:
                    if mark:
                        jo.write(" -------------- TABLE ------------\n")
                    print("table", table["type"], table.keys())

                    if "title" in table:
                        for s in tokenize(table["title"]):
                            jo.write(s + "\n")

                    if "text-tags" in table:
                        for t in table["text-tags"]:
                            for s in tokenize(t[0]):
                                jo.write(s + "\n")

                    if "children" in table:
                        for tableLine in table["children"]:
                            if mark:
                                jo.write(" -------------- TABLELINE ------------\n")
                            print(tableLine["type"], tableLine.keys())

                            if "title" in tableLine:
                                for s in tokenize(tableLine["title"]):
                                    #jo.write(s + "\n")
                                    pass

                            if "text-tags" in tableLine:
                                for t in tableLine["text-tags"]:
                                    for s in tokenize(t[0]):
                                        jo.write(s + "\n")


                            if "children" in tableLine:
                                for cell in tableLine["children"]:
                                    if mark:
                                        jo.write(" -------------- CELL ------------\n")
                                    print(cell["type"], cell.keys())

                                    if "title" in cell:
                                        for s in tokenize(cell["title"]):
                                            jo.write(s + "\n")




    print(data["data"][0]["children"][0]["title"])


def find_in_json(word, dict):
    if "title" in dict:
        #print(dict["title"])
        if word in dict["title"]:
            print(dict["title"])
    if "text-tags" in dict:
        for text in dict["text-tags"]:
            if word in text:
                print("Found", text)
    if "children" in dict:
        for child in dict["children"]:
            find_in_json(word, child)

def find_words(node):
    if node.tag.split("}")[1] == "wd":
        if not node.text:
            print(node.attrib, node.text)
        else:
            for c in tokenize(node.text):
                #xo.write(c + "\n")
                pass
            xo.write(node.text + "\n")
            print("Searching for", node.text)
            find_in_json(node.text, data["data"][0])
            time.sleep(1)
        #print(node.attrib, node.text)
    else:
        for child in node.getchildren():
            find_words(child)

def omni_coords_to_normal(omni_coord_value, image_dpi=300):
    res = int((omni_coord_value * image_dpi) / 1440)
    return res

def tokenize(str):
    tokens = []
    token = ""
    for c in str:
        if c in string.punctuation:
            if not token == "":
                tokens.append(token)
            tokens.append(c)
            token = ""
        elif c == " ":
            if not token == "":
                tokens.append(token)
            token = ""
        else:
            token += c
    if not token == "":
        tokens.append(token)

    return tokens

main()
