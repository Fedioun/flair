from flair.data import Sentence
from flair.models import SequenceTagger
from flair.datasets import ColumnCorpus
from flair.data import Corpus
import os
import time
import tqdm

def main():

    # 1. get the corpus
    columns = {0: 'text', 1 : "pos"}
    rubric = "CAPITAL"

    nb_cells = 16
    model_name = str(nb_cells)+ "_01"

    # this is the folder in which train, test and dev files reside
    id = "EHF_" + rubric + "_dataset_v0"
    data_folder = './datasets/' + id

    # init a corpus using column format, data folder and the names of the train, dev and test files
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                                  train_file="train_" + id + '.txt',
                                  test_file="test_" + id + '.txt',
                                  dev_file="valid_" + id + '.txt')

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

    tagger: SequenceTagger = SequenceTagger.load("./resources/taggers/" + model_name + "/best-model.pt")

    output_file = "./predictions/" + model_name + "/" + "test_" + id + ".txt"
    write_predictions(corpus.test.sentences, tagger, tags, output_file)

    output_file = "./predictions/" + model_name + "/" + "test_" + id + ".md"
    visualize(corpus.test.sentences, tags, output_file)

    #print("Analysing %s" % sentence)






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
                        out.write(token +" None\n")
                    token = t
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

main()
