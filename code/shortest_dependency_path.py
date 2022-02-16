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

nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")


def find_shortest_path(text_list):
    df_list = []
    # Load spacy's dependency tree into a networkx graph
    for sentence in text_list:
        edges = []
        doc = nlp(sentence)

        """ subject and direct object from sentence """
        subject = [tok for tok in doc if (tok.dep_ == "nsubj")]
        direct_object = [tok for tok in doc if (tok.dep_ == "dobj")]

        if (len(direct_object) < 1) or (len(subject) < 1):
            df_list.append({"sentence": sentence, "first_entity": None, "second_entity": None, "shortest_path": None})
            continue

        else:
            subject = subject[0]
            direct_object = direct_object[0]
            for token in doc:
                for child in token.children:
                    edges.append(('{0}'.format(token.lower_),
                                  '{0}'.format(child.lower_)))

            graph = nx.Graph(edges)

            entity1 = str(subject).lower()
            entity2 = str(direct_object).lower()
            shortest_path = nx.shortest_path(graph, source=entity1, target=entity2)
            df_list.append({"sentence": sentence, "first_entity": entity1, "second_entity": entity2,
                            "shortest_path": shortest_path})

    final_df = pd.DataFrame(df_list)
    return final_df


if __name__ == "__main__":

    with open("../data/article.txt", encoding="utf-8") as f:
        content = f.read()

    # convert text into a list of sentences
    text_list_input = nltk.tokenize.sent_tokenize(content)
    shortest_path_results = find_shortest_path(text_list_input)
    shortest_path_results.to_csv("../data/shortest_path.csv")
    print('DONE')
