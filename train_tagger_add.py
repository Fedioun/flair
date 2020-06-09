from typing import List

import flair.datasets
from flair.datasets import ColumnCorpus
from flair.data import Corpus
from flair.embeddings import (
    TokenEmbeddings,
    WordEmbeddings,
    StackedEmbeddings,
    FlairEmbeddings,
    CharacterEmbeddings,
    FloatsEmbeddings
)
from flair.training_utils import EvaluationMetric
from flair.visual.training_curves import Plotter

from predict_tagger import predict_tagger
import os



def main():

    datasets = os.listdir("./datasets")
    print(datasets)
    language = "fr"

    nb_cells = 32
    dataset = "DESFOSSE_ARRAY"

    exp_name = dataset + "_" + str(nb_cells)
    # 1. get the corpus
    columns = {0: 'text', 1: 'position', 2 : "array", 3 : "line", 4 : "col"}

    # this is the folder in which train, test and dev files reside
    data_folder = './datasets/' + dataset

    # init a corpus using column format, data folder and the names of the train, dev and test files
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                                  train_file="train_" + dataset + '.txt',
                                  test_file="test_"  + dataset + '.txt',
                                  dev_file="valid_"  + dataset + '.txt')

    print(corpus)

    # 2. what tag do we want to predict?
    tag_type = "col"

    exp_name = dataset + "_" + tag_type

    # 3. make the tag dictionary from the corpus
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
    print(tag_dictionary.idx2item)

    # initialize embeddings
    embedding_types: List[TokenEmbeddings] = []
    embedding_types.append(FlairEmbeddings(language + '-forward'))
    embedding_types.append(FlairEmbeddings(language + '-backward'))
    embedding_types.append(FloatsEmbeddings(field='position', length=4))

    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)



    # initialize sequence tagger
    from flair.models import SequenceTagger

    tagger: SequenceTagger = SequenceTagger(
        hidden_size=nb_cells,
        embeddings=embeddings,
        tag_dictionary=tag_dictionary,
        tag_type=tag_type,
        use_crf=True,
    )

    # initialize trainer
    from flair.trainers import ModelTrainer

    trainer: ModelTrainer = ModelTrainer(tagger, corpus)

    trainer.train(
        "resources/taggers/" + exp_name,
        learning_rate=0.1,
        embeddings_storage_mode= "cpu",
        mini_batch_size=32,
        max_epochs=150,
        shuffle=False,
    )

    plotter = Plotter()
    plotter.plot_training_curves("resources/taggers/" + exp_name + "/loss.tsv")
    plotter.plot_weights("resources/taggers/" + exp_name + "/weights.txt")

    predict_tagger(setId, nb_cells, rubric, rubric)

main()
