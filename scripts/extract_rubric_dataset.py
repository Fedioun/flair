import json
import mysql.connector
import time
import os



def main():
    remote = False

    if remote:
        host = "mutzschen.univ-rouen.fr"
        port = 3306
        user = "eurhisfirm"
        database = "pivan_" + user
        password = "Saib!aix1ieMa;e"
        "fi.Fupheilue3be"
    else:
        host = "localhost"
        port = 3306
        user = "pivan"
        database = "pivan_eurhisfirm"
        password = "pivan"

    dir_name = "./datasets/EHF_category_dataset"

    elts = [
        "Token.global_id",
        "Token.wc",
        "Correction.new_content",
        "Correction.old_content",
        #"Correction.created"
    ]
    global_id_prefix = "COTE-MARCHE_18990616_01"

    try:
        mydb = mysql.connector.connect(
          host=host,
          user=user,
          passwd=password,
          database=database
        )
    except Exception as e:
        print(e)
        print("Cannot connect to the db")
        exit(1)
    print("Successfully connected to " + database)


    ###############################################

    elts = [
        "Token.global_id",
        "Token.wc",
        "Token.text_content"
    ]

    mycursor = mydb.cursor()

    query = "SELECT distinct Token.*, TokenExtra.* FROM TokenExtra, Token "\
    + "WHERE Token.id = TokenExtra.id "
    #+ "AND Token.id = TokenExtra.id "

    print("Start query")
    mycursor.execute(query)

    myresult = mycursor.fetchall()
    print(str(len(myresult)) + " results fetched")
    prefix = ""

    try:
        os.makedirs(dir_name)
    except Exception as e:
        print(e)


    dict = {}
    ids = []
    for x in myresult:
        id = x[12]

        if not id in ids:
            if not id.split("-")[0] in dict:
                dict[id.split("-")[0]] = {}

            if not id.split("-")[1] in dict[id.split("-")[0]]:
                dict[id.split("-")[0]][id.split("-")[1]] = {}

            if not id.split("-")[2] in dict[id.split("-")[0]][id.split("-")[1]]:
                dict[id.split("-")[0]][id.split("-")[1]][id.split("-")[2]] = []

            dict[id.split("-")[0]][id.split("-")[1]][id.split("-")[2]].append(x[9])

            ids.append(x[12])

    size = len(dict)
    train_size = size * 0.8
    eval_size = size * 0.1
    print(train_size)
    n = 0
    for page in dict:
        if n < train_size:
            set = "train"
        elif n >= train_size and n < train_size + eval_size:
            set = "dev"
        else:
            set = "test"

        output_file = os.path.join(dir_name, set + "_both_" + dir_name.split("/")[-1] + ".txt")
        write_to_file(output_file, dict[page], True, True)
        output_file = os.path.join(dir_name, set + "_start_" + dir_name.split("/")[-1] + ".txt")
        write_to_file(output_file, dict[page], True, False)
        output_file = os.path.join(dir_name, set + "_" + dir_name.split("/")[-1] + ".txt")
        write_to_file(output_file, dict[page], False, False)
        n += 1



    print("Job done !")

def write_to_file(output_file, page, start, end):
    with open(output_file, "a", encoding="utf8") as out:
        for category in page:

            last = False
            for rubric in page[category]:
                #tag = category.split("_")[0].replace(" ", "_")
                tag = rubric.split("_id")[0].replace(" ", "_")
                tagTokens = (rubric.split("_id")[0] + " :").split(" ")

                for token in tagTokens:
                    if start :
                        out.write(token + " start_" + tag + "\n")
                    else:
                        out.write(token + " " + tag + "\n")

                for i, token in enumerate(page[category][rubric]):
                    if end and i == len(page[category][rubric]) - 1:
                        out.write(token + " end_" + tag + "\n")
                    else:
                        out.write(token + " " + tag + "\n")
        out.write("\n")



main()
