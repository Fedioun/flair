import os



def main():
    dataset_folder = "/home/nosmoth/Dev/flair/datasets/"

    datasets = os.listdir(dataset_folder)


    for dataset in datasets:
        files = os.listdir(os.path.join(dataset_folder, dataset))

        for file in files :
            if file.startswith("test"):
                nb_accent = 0
                nb_char = 0

                with open(os.path.join(dataset_folder, dataset, file), "r", encoding="utf8") as f:
                    lines = f.readlines()
                    for line in lines:
                        token = line.split(" ")[0]
                        for char in token:
                            nb_char += 1
                            if ord(char) > 190:
                                nb_accent += 1
        print(dataset + " : accents " + str(nb_accent) + "  chars " + str(nb_char) + "  ratio " + str(nb_accent/nb_char))

# EHF_Exploitation 3.8%


main()
