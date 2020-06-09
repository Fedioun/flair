import os
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def main():
    dataset_folder = "/home/nosmoth/Dev/flair/datasets/"


    datasets = os.listdir(dataset_folder)
    output_name = "EHF_EXPLOITATION_normalised"

    if not os.path.isdir(os.path.join(dataset_folder, output_name)):
        os.mkdir(os.path.join(dataset_folder, output_name))

    for dataset in datasets:
        files = os.listdir(os.path.join(dataset_folder, dataset))
        if dataset != "EHF_EXPLOITATION_dataset_v0":
            continue


        for file in files :
            if "test" in  file:
                out = open(os.path.join(dataset_folder, output_name, "test.txt"), "w", encoding="utf8")
            if "train" in  file:
                out = open(os.path.join(dataset_folder, output_name, "train.txt"), "w", encoding="utf8")
            if "valid" in  file:
                out = open(os.path.join(dataset_folder, output_name, "valid.txt"), "w", encoding="utf8")


            with open(os.path.join(dataset_folder, dataset, file), "r", encoding="utf8") as f:
                lines = f.readlines()
                for line in lines:
                    token = line.split(" ")[0]
                    out.write(remove_accents(token) + " " + " ".join(line.split(" ")[1:]))


# EHF_Exploitation 3.8%


main()
