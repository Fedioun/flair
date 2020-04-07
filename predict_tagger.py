from flair.data import Sentence
from flair.models import SequenceTagger
from flair.datasets import ColumnCorpus
from flair.data import Corpus
import os
import time
import tqdm

from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt

def main():
    rubric = "CAPITAL"
    nb_cells = 16

    sets = os.listdir("./datasets")
    for set in sets:
        nb_cells = 16
        if set.split("_")[0] != "EHF":
            continue

        if set.split("_")[1] == "shuffled":
            continue
            nb_cells = 32

        print(set)
        if set.split("_")[1] == "category" :
            continue

        predict_tagger(
            setId=set.split("_")[0],
            nb_cells=32,
            rubric=set.split("_")[1],
            model="shuffled"
        )




def predict_tagger(setId, nb_cells, rubric, model):
    # 1. get the corpus
    columns = {0: 'text', 1 : "pos"}

    suffix = "_dataset"

    model_name = model + "_" + str(nb_cells)+ "_01"

    # this is the folder in which train, test and dev files reside
    id = setId + "_" + rubric + suffix + "_v0"
    data_folder = './datasets/' + id

    # init a corpus using column format, data folder and the names of the train, dev and test files
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                                  train_file="train" + "_" + id + '.txt',
                                  test_file="test"+ "_" + id + '.txt',
                                  dev_file="valid" + "_" + id + '.txt')

    print(len(corpus.test.sentences))

    # 2. what tag do we want to predict?
    tag_type = "pos"

    # 3. make the tag dictionary from the corpus
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
    tags = [ '<'  + x.decode("UTF-8") + ">" for x in tag_dictionary.idx2item]

    if not os.path.isdir("./predictions"):
        os.mkdir("./predictions")
    if not os.path.isdir("./predictions/" + model_name):
        os.mkdir("./predictions/" + model_name)

    output_file = "./predictions/" + "test_" + id + "_ground_truth.md"
    visualize(corpus.test.sentences, tags, output_file)

    # Get y_true
    classes = []
    y_true = []

    y_truths = []
    for sentence in corpus.test.sentences:
        y = []
        for token in sentence.tokens:
            if not token.tags['pos'].value in classes:
                classes.append(token.tags['pos'].value)
            y.append(token.tags['pos'].value)
        y_truths.append(y)

    y_true = [tag for y_true in y_truths for tag in y_true]

    # Load pred model
    tagger: SequenceTagger = SequenceTagger.load("./resources/taggers/" + model_name + "/best-model.pt")

    output_file = "./predictions/" + model_name + "/" + "test_" + id + ".txt"

    # If already predicted, use the file
    test_file = "test"+ "_" + id + '.txt'
    try:
        corpus = ColumnCorpus("./predictions/" + model_name, columns, test_file=test_file, train_file=test_file, dev_file = test_file)
    except Exception as e:
        print(e)
        write_predictions(corpus.test.sentences, tagger, tags, output_file)

    # Get y_pred
    y_preds = []
    for sentence in corpus.test.sentences:
        y = []
        for token in sentence.tokens:
            if not token.tags['pos'].value in classes:
                classes.append(token.tags['pos'].value)
            y.append(token.tags['pos'].value)
        y_preds.append(y)

    y_pred = [tag for y_pred in y_preds for tag in y_pred]

    # Metrics
    precision, recall, f1, nb_chunk, nb_pred_chunk, nb_good_pred_chunk = compute_chunks_metric(y_truths, y_preds)

    output_file = "./predictions/" + model_name + "/" + "chunksMetric.txt"
    with open(output_file, "w", encoding="utf8") as out:
        out.write(str(nb_chunk) +  " in ground_truth"+ "\n")
        out.write(str(nb_pred_chunk)+ " in prediction"+ "\n")
        out.write(str(nb_good_pred_chunk)+ " correctly predicted"+ "\n\n")
        out.write("Precision : "+ str(precision)+ "\n")
        out.write("Recall : "+ str(recall)+ "\n")
        out.write("F1 : "+ str(f1)+ "\n")


    # Beautiful graphics
    output_file = "./predictions/" + model_name + "/" + "test_" + id + ".md"
    visualize(corpus.test.sentences, tags, output_file)

    cm = confusion_matrix(y_true, y_pred, labels=classes)
    #cm[classes.index("O")][classes.index("O")] = -1
    fig, ax = plot_confusion_matrix(conf_mat=cm, colorbar=True,class_names=classes, show_absolute=False, show_normed=True, figsize=(6 + len(classes) * 0.4, 6 + len(classes) * 0.4))
    plt.savefig("./cms/" + setId + "_" + rubric + ".png")

    #print("Analysing %s" % sentence)


'''
    y_truths and y_preds : list of sentences
    sentences are composed of a list of tags
'''
def compute_chunks_metric(y_truths, y_preds):
    # Check integrity
    assert(len(y_truths) == len(y_preds))
    for y in range(len(y_truths)):
        assert(len(y_truths[y]) - len(y_preds[y]) == 0)

    nb_chunk = 0
    nb_pred_chunk = 0
    nb_good_pred_chunk = 0
    # Pour chaque rubrique
    for i in range(len(y_truths)):
        chunk = False
        predChunk = False
        lastPredToken = "O"
        valid = True
        #print(chunk)
        # Pour chaque token
        for k in range(len(y_truths[i])):
            #print("LastPredToken : ", lastPredToken)
            # Entering true  chunk
            if chunk == False and not y_truths[i][k] == "O":
                #print("entering chunk", y_truths[i][k])
                chunk = True
                if lastPredToken == "O" and y_preds[i][k] == y_truths[i][k]:
                    valid = True

            # Check identity of tag
            if not y_preds[i][k] == y_truths[i][k]:
                valid = False

            # Entering predicted chunk
            if predChunk == False and not y_preds[i][k] == "O":
                predChunk = True

            # Leaving chunk
            if predChunk == True and y_preds[i][k] == "O":
                nb_pred_chunk += 1
                predChunk = False

            # Leaving chunk
            if chunk == True and y_truths[i][k] == "O":
                #print("leaving chunk")
                chunk = False
                if valid:
                    nb_good_pred_chunk += 1
                nb_chunk += 1
            lastPredToken = y_preds[i][k]
    print("Nb true chunk : ", nb_chunk,  "Nb pred chunk : ", nb_pred_chunk, "Nb correctly predicted chunk : ", nb_good_pred_chunk)

    tp = nb_good_pred_chunk
    fp = nb_pred_chunk - tp
    fn = nb_chunk - nb_good_pred_chunk

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * ((precision * recall) / (precision + recall))

    print("precision : ", precision)
    print("recall : ", recall)
    print("F1 score : ", f1)
    return precision, recall, f1, nb_chunk, nb_pred_chunk, nb_good_pred_chunk


def write_predictions(sentences, tagger, tags, file):
    with open(file, "w", encoding="utf8") as out:
        for sentence in tqdm.tqdm(sentences):
            tagger.predict(sentence)

            '''
            for t in sentence.tokens:
                print(t.get_tag("pos"))
                time.sleep(0.5)
            '''
            token = ""
            for t in sentence.to_tagged_string().split(" "):

                if t in tags:
                    color = get_color(palette, tags, t)
                    out.write(token + " " + t[1:-1] + "\n")
                    token = ""
                else:
                    if not token == "":
                        out.write(token +" O\n")
                    token = t
            if not token == "":
                out.write(token +" O\n")
            out.write("\n")



def visualize(sentences, tags, file):
    with open(file, "w", encoding="utf8") as out:
        for sentence in tqdm.tqdm(sentences):
            token = ""
            for t in sentence.to_tagged_string().split(" "):
                if t in tags:
                    color = get_color(palette, tags, t)
                    out.write("<span style=\"color:rgb(" + str(color[0]) + "," + str(color[1])+ "," + str(color[2]) + ")\">" + token + "</span> ")
                    token = ""
                else:
                    if not token == "":
                        out.write(token +" ")
                    token = t
            out.write("\n\n\n")

def get_sentences(file) :
    sentences = []
    with open(file, "r", encoding='utf8') as input:
        lines = input.readlines()
        str = ""
        for line in lines:
            if len(line) == 1:
                sentences.append(Sentence(str))
                str = ""
            else:
                str += line.split(" ")[0] + " "
    return sentences



def get_color(palette, tags, tag):
    pos = 3 * tags.index(tag)
    return (palette[pos], palette[pos+1], palette[pos+2])

palette = [0, 0, 0, 128, 0, 0, 0, 128, 0, 128, 128, 0, 0, 0, 128, 128, 0, 128, 0, 128, 128, 128, 128, 128, 64, 0, 0,
           192, 0, 0, 64, 128, 0, 192, 128, 0, 64, 0, 128, 192, 0, 128, 64, 128, 128, 192, 128, 128, 0, 64, 0, 128, 64,
           0, 0, 192, 0, 128, 192, 0, 0, 64, 128, 128, 64, 128, 0, 192, 128, 128, 192, 128, 64, 64, 0, 192, 64, 0, 64,
           192, 0, 192, 192, 0, 64, 64, 128, 192, 64, 128, 64, 192, 128, 192, 192, 128, 0, 0, 64, 128, 0, 64, 0, 128,
           64, 128, 128, 64, 0, 0, 192, 128, 0, 192, 0, 128, 192, 128, 128, 192, 64, 0, 64, 192, 0, 64, 64, 128, 64,
           192, 128, 64, 64, 0, 192, 192, 0, 192, 64, 128, 192, 192, 128, 192, 0, 64, 64, 128, 64, 64, 0, 192, 64, 128,
           192, 64, 0, 64, 192, 128, 64, 192, 0, 192, 192, 128, 192, 192, 64, 64, 64, 192, 64, 64, 64, 192, 64, 192,
           192, 64, 64, 64, 192, 192, 64, 192, 64, 192, 192, 192, 192, 192, 32, 0, 0, 160, 0, 0, 32, 128, 0, 160, 128,
           0, 32, 0, 128, 160, 0, 128, 32, 128, 128, 160, 128, 128, 96, 0, 0, 224, 0, 0, 96, 128, 0, 224, 128, 0, 96, 0,
           128, 224, 0, 128, 96, 128, 128, 224, 128, 128, 32, 64, 0, 160, 64, 0, 32, 192, 0, 160, 192, 0, 32, 64, 128,
           160, 64, 128, 32, 192, 128, 160, 192, 128, 96, 64, 0, 224, 64, 0, 96, 192, 0, 224, 192, 0, 96, 64, 128, 224,
           64, 128, 96, 192, 128, 224, 192, 128, 32, 0, 64, 160, 0, 64, 32, 128, 64, 160, 128, 64, 32, 0, 192, 160, 0,
           192, 32, 128, 192, 160, 128, 192, 96, 0, 64, 224, 0, 64, 96, 128, 64, 224, 128, 64, 96, 0, 192, 224, 0, 192,
           96, 128, 192, 224, 128, 192, 32, 64, 64, 160, 64, 64, 32, 192, 64, 160, 192, 64, 32, 64, 192, 160, 64, 192,
           32, 192, 192, 160, 192, 192, 96, 64, 64, 224, 64, 64, 96, 192, 64, 224, 192, 64, 96, 64, 192, 224, 64, 192,
           96, 192, 192, 224, 192, 192, 0, 32, 0, 128, 32, 0, 0, 160, 0, 128, 160, 0, 0, 32, 128, 128, 32, 128, 0, 160,
           128, 128, 160, 128, 64, 32, 0, 192, 32, 0, 64, 160, 0, 192, 160, 0, 64, 32, 128, 192, 32, 128, 64, 160, 128,
           192, 160, 128, 0, 96, 0, 128, 96, 0, 0, 224, 0, 128, 224, 0, 0, 96, 128, 128, 96, 128, 0, 224, 128, 128, 224,
           128, 64, 96, 0, 192, 96, 0, 64, 224, 0, 192, 224, 0, 64, 96, 128, 192, 96, 128, 64, 224, 128, 192, 224, 128,
           0, 32, 64, 128, 32, 64, 0, 160, 64, 128, 160, 64, 0, 32, 192, 128, 32, 192, 0, 160, 192, 128, 160, 192, 64,
           32, 64, 192, 32, 64, 64, 160, 64, 192, 160, 64, 64, 32, 192, 192, 32, 192, 64, 160, 192, 192, 160, 192, 0,
           96, 64, 128, 96, 64, 0, 224, 64, 128, 224, 64, 0, 96, 192, 128, 96, 192, 0, 224, 192, 128, 224, 192, 64, 96,
           64, 192, 96, 64, 64, 224, 64, 192, 224, 64, 64, 96, 192, 192, 96, 192, 64, 224, 192, 192, 224, 192, 32, 32,
           0, 160, 32, 0, 32, 160, 0, 160, 160, 0, 32, 32, 128, 160, 32, 128, 32, 160, 128, 160, 160, 128, 96, 32, 0,
           224, 32, 0, 96, 160, 0, 224, 160, 0, 96, 32, 128, 224, 32, 128, 96, 160, 128, 224, 160, 128, 32, 96, 0, 160,
           96, 0, 32, 224, 0, 160, 224, 0, 32, 96, 128, 160, 96, 128, 32, 224, 128, 160, 224, 128, 96, 96, 0, 224, 96,
           0, 96, 224, 0, 224, 224, 0, 96, 96, 128, 224, 96, 128, 96, 224, 128, 224, 224, 128, 32, 32, 64, 160, 32, 64,
           32, 160, 64, 160, 160, 64, 32, 32, 192, 160, 32, 192, 32, 160, 192, 160, 160, 192, 96, 32, 64, 224, 32, 64,
           96, 160, 64, 224, 160, 64, 96, 32, 192, 224, 32, 192, 96, 160, 192, 224, 160, 192, 32, 96, 64, 160, 96, 64,
           32, 224, 64, 160, 224, 64, 32, 96, 192, 160, 96, 192, 32, 224, 192, 160, 224, 192, 96, 96, 64, 224, 96, 64,
           96, 224, 64, 224, 224, 64, 96, 96, 192, 224, 96, 192, 96, 224, 192, 224, 224, 192]
if __name__ == '__main__':
    main()
