import json, os, random






def main():

    generate_shuffled_dataset(
        setId="HB",
        input_folder="/home/nosmoth/Documents/EurHisFirm/" +  "HandBuch",
    )
    exit()
    input_folder = "/home/nosmoth/Documents/EurHisFirm/" + "HandBuch_v2"#"datasets_french_rubrics" #
    rubricFiles = os.listdir(input_folder)
    setId = "HB"

    for rubricFile in rubricFiles:
        print(rubricFile)
        rubric = (rubricFile.split("_")[1]).split(".")[0]

        input_file =  os.path.join(input_folder, rubricFile)

        dataset_folder = "./datasets"
        output_folder = setId + "_" + rubric + "_dataset_v0"

        if not os.path.isdir(dataset_folder):
            os.mkdir(dataset_folder)

        if not os.path.isdir(os.path.join(dataset_folder, output_folder)):
            os.mkdir(os.path.join(dataset_folder, output_folder))

        classes = []

        with open(input_file, "r", encoding="utf8") as f:
            data = json.load(f)

            sets = ["train", "valid", "test"]
            for set in sets:
                output_file = os.path.join(dataset_folder, output_folder, set + "_" + output_folder + ".txt")
                with open(output_file, "w", encoding="utf8") as out:


                    for rubric in data[set + "-dataset"]:
                        for token in rubric["text-tags"]:
                            #print(token)
                            if not token[1] in classes:
                                classes.append(token[1])

                            if not str(token[0]) == " " and not str(token[0]) == "":
                                out.write(str(token[0]) + " " + token[1] + " " + str(classes.index(token[1])) + "\n")
                        out.write("\n")

def generate_shuffled_dataset(
        setId="HB",
        input_folder="/home/nosmoth/Documents/EurHisFirm/" +  "HandBuch",
    ):
    "datasets_french_rubrics"
    "HandBuch"
    id = setId + "_shuffled_dataset_v1"

    dataset_folder = "./datasets/" + id

    if not os.path.isdir(dataset_folder):
        os.mkdir(dataset_folder)

    files = os.listdir(input_folder)
    dataset = {
        "train" : [],
        "valid" : [],
        "test" : []
    }
    for file in files :
        if file.startswith("datasets_"):
            with open(os.path.join(input_folder, file), "r", encoding="utf8") as f:
                data = json.load(f)
                for set in dataset.keys():
                    for rubric in data[set + "-dataset"]:
                        dataset[set].append(rubric["text-tags"])

    for set in dataset.keys():
        random.shuffle(dataset[set])
        output_file = os.path.join(dataset_folder, set + "_" + id + ".txt")
        with open(output_file, "w", encoding="utf8") as out:
            for rubric in dataset[set]:
                for token in rubric:
                    if not str(token[0]) == " " and not str(token[0]) == "" and not str(token[0]) == "  ":
                        out.write(str(token[0]) + " " + token[1] + "\n")
                out.write("\n")




main()
