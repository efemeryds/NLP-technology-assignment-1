"""
- source: https://towardsdatascience.com/how-to-find-shortest-dependency-path-with-spacy-and-stanfordnlp-539d45d28239
- definition of the feature:
    Semantic dependency parsing had been frequently used to dissect sentence and to capture word semantic information
    close in context but far in sentence distance. To extract the relationship between two entities, the most direct
    approach is to use SDP. The motivation of using SDP is based on the observation that the SDP between entities
    usually contains the necessary information to identify their relationship.
- libraries to install:
    pip install spacy
    python3 -m spacy download en_core_web_sm
    pip install stanfordnlp
    pip install networkx
"""

import nltk
import spacy
import networkx as nx
import pandas as pd
import stanza
# import matplotlib.pyplot as plt
# stanza.download('en')

nltk.download('punkt')
sub_labels = []


def syntax(text_list):
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency')
    tree_list = []
    for sentence in text_list:
        doc = nlp(sentence)
        tree = doc.sentences[0].constituency
        tree_list.append(tree)
    return tree_list


def find_shortest_path(text_list):
    nlp = spacy.load("en_core_web_sm")
    first_list = []
    second_list = []
    path_list = []
    # Load spacy's dependency tree into a networkx graph
    for sentence in text_list:
        edges = []
        doc = nlp(sentence)

        """ subject and direct object from sentence """
        subject = [tok for tok in doc if (tok.dep_ == "nsubj")]
        direct_object = [tok for tok in doc if (tok.dep_ == "dobj")]

        if (len(direct_object) < 1) or (len(subject) < 1):
            first_list.append(None)
            second_list.append(None)
            path_list.append(None)
            continue

        else:
            subject = subject[0]
            direct_object = direct_object[0]
            for token in doc:
                for child in token.children:
                    edges.append(('{0}'.format(token.lower_),
                                  '{0}'.format(child.lower_)))

            graph = nx.Graph(edges)

            # pos = nx.spring_layout(graph)
            # nx.draw_networkx_edges(graph, pos, arrows=False)
            # plt.show()

            entity1 = str(subject).lower()
            entity2 = str(direct_object).lower()
            shortest_path = nx.shortest_path(graph, source=entity1, target=entity2)
            first_list.append(entity1)
            second_list.append(entity2)
            path_list.append(shortest_path)

    return first_list, second_list, path_list


if __name__ == "__main__":

    with open("../data/article.txt", encoding="utf-8") as f:
        content = f.read()

    # convert text into a list of sentences
    text_list_input = nltk.tokenize.sent_tokenize(content)
    tree = syntax(text_list_input)
    first, second, path = find_shortest_path(text_list_input)
    results = pd.DataFrame({"sentence": text_list_input,
                            "full_tree": tree,
                            "first_entity": first,
                            "second_entity": second,
                            "shortest_dep_path": path})
    results.to_csv("../results/sentence_features.csv")
    print('DONE')
