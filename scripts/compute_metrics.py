
import time
import numpy as np

def main():
    type = ""
    nb_cells = 32
    ground_truth_file = "./datasets/EHF_category_dataset/test_" + type + "EHF_category_dataset.txt"
    prediction_file = "./predictions/" + type + "ss_rubric_" + str(nb_cells) + "_01/test_EHF_category_dataset.txt"

    with open(ground_truth_file, "r", encoding="utf8") as ground_truth:
        truth_lines = ground_truth.readlines()

    with open(prediction_file, "r", encoding="utf8") as predictions:
        predictions_lines = predictions.readlines()

    rubric_count = 0
    bad_rubric = 0
    almost_bad_rubric = 0
    error_tab_size = 10
    error_tab = np.zeros(error_tab_size)
    nb_error = 0
    previous_tag = ""
    for k in range(len(truth_lines)):
        truth = truth_lines[k].split(" ")
        prediction = predictions_lines[k].split(" ")

        if not truth[0] == prediction[0]:
            print("Bad alignment, check files")
            exit(0)
        if len(truth) > 1:
            if type == "start_":
                if truth[1].startswith("start_"):
                    for k in range(error_tab_size):
                        if nb_error > k:
                            error_tab[k] += 1
                    rubric_count += 1
                    nb_error = 0
            else:
                if truth[1] != previous_tag:
                    for k in range(error_tab_size):
                        if nb_error > k:
                            error_tab[k] += 1
                    rubric_count += 1
                    nb_error = 0
                    previous_tag = truth[1]

            if not truth[1].strip() == prediction[1].strip():
                nb_error += 1
                #print(truth[1], prediction[1])
                #time.sleep(0.5)

    for k in range(error_tab_size):
        if nb_error > k:
            error_tab[k] += 1

    for k in range(error_tab_size):
        print(k, rubric_count, error_tab[k], 1 - error_tab[k]/rubric_count)


main()
