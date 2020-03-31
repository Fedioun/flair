import json, os, random






def main():
    generate_shuffled_dataset()
    exit()
    rubric = "CHIFFRE_D_AFFAIRES"
    file =  "datasets_" + rubric + ".json"
    input_folder = "/home/nosmoth/Documents/EurHisFirm/" + "datasets_french_rubrics"
    input_file =  os.path.join(input_folder, file)

    dataset_folder = "./datasets"
    output_folder = "EHF_" + file.split("_")[1].split(".")[0] + "_dataset_v0"
    output_fle = os.path.join(dataset_folder, output_folder)

    if not os.path.isdir(dataset_folder):
        os.mkdir(dataset_folder)

    if not os.path.isdir(os.path.join(dataset_folder, output_folder)):
        os.mkdir(os.path.join(dataset_folder, output_folder))

    with open(input_file, "r", encoding="utf8") as f:
        data = json.load(f)

        sets = ["train", "valid", "test"]
        for set in sets:
            output_file = os.path.join(dataset_folder, output_folder, set + "_" + output_folder + ".txt")
            with open(output_file, "w", encoding="utf8") as out:


                for rubric in data[set + "-dataset"]:
                    for token in rubric["text-tags"]:
                        print(token)
                        out.write(str(token[0]) + " " + token[1] + "\n")
                    out.write("\n")

def generate_shuffled_dataset():
    input_folder = "/home/nosmoth/Documents/EurHisFirm/" + "datasets_french_rubrics"
    dataset_folder = "./datasets/EHF_shuffled_v0"

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
        output_file = os.path.join(dataset_folder, set + ".txt")
        with open(output_file, "w", encoding="utf8") as out:
            for rubric in dataset[set]:
                for token in rubric:
                    out.write(str(token[0]) + " " + token[1] + "\n")
                out.write("\n")




main()
