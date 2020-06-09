
import json
import mysql.connector
import time
import os
import numpy as np


def main():
    host = "localhost"
    port = 3306
    user = "pivan"
    database = "pivan_eurhisfirm"
    password = "pivan"

    output_file = "DESFOSSE.txt"

    output_folder = "DESFOSSE"

    if not os.path.exists("./datasets"):
        os.mkdir("./datasets")

    if not os.path.exists(os.path.join("./datasets", output_folder)):
        os.mkdir(os.path.join("./datasets", output_folder))





    cnx = mysql.connector.MySQLConnection(
        user=user,
        password=password,
        host=host,
        database=database,
        port=port
    )
    title = ""

    query = "SELECT Page.id, Page.w, Page.h FROM Page, Issue, Title WHERE Page.issue = Issue.id AND Issue.title = Title.id AND Title.shortname='FRYB';"
    cursor = cnx.cursor()
    cursor.execute(query)
    pages = np.array(cursor.fetchall())
    print(pages)

    cursor.close()
    n = 0
    set = "train"
    out =  open(os.path.join("./datasets", output_folder, set + "_" + output_file), "w", encoding="utf8")
    for page in pages:
        print(n, set)
        if n > 0.8 * len(pages) and n <= 0.9 * len(pages) and not set == "test" :
            set = "test"
            out.close()
            out =  open(os.path.join("./datasets", output_folder, set + "_" + output_file), "w", encoding="utf8")
        if n > 0.9 * len(pages) and not set == "valid":
            set = "valid"
            out.close()
            out =  open(os.path.join("./datasets", output_folder, set + "_" + output_file), "w", encoding="utf8")
        query = "SELECT  Token.text_content, CRFTag.label, Category.Label, Line.x, Line.y, Line.h, Line.w, Token.id From CRFTag, TokenExtra, Category, Region, Line, Token WHERE TokenExtra.id = Token.id AND TokenExtra.crfTag = CRFTag.id AND Category.id = CRFTag.category AND Token.line = Line.id AND Line.text = Region.id AND Region.page = " + str(page[0]) + " ORDER BY Token.id"
        cursor = cnx.cursor()
        cursor.execute(query)
        page = np.array(cursor.fetchall())
        cursor.close()


        for token in page :
            out.write(token[0] + " " + token[1] + " " + token[2].split(".", 1)[1] + " [" + str(token[3]) + "," + str(token[4]) + "," + str(token[5]) + "," + str(token[6]) + "]\n")


        out.write("\n")
        n+= 1
    out.close()

    cnx.close()
main()
