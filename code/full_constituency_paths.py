import spacy
import nltk
import pandas as pd
import stanza

# run in terminal, if you don't have the package: python3 -m spacy download en_core_web_sm

def prepare_data(text_path):
    with open(text_path, encoding="utf-8") as f:
        content = f.read()

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(content)

    # https://spacy.io/api/token
    token = [tok.text for tok in doc]
    dependency = [tok.dep_ for tok in doc]
    head = [tok.head for tok in doc]
    dependent = [[t.text for t in tok.children] for tok in doc]
    constituent = [[t.text for t in tok.subtree] for tok in doc]

    parse_info = {"token": token, "dependency": dependency,
                  "head": head, "dependent": dependent,
                  "constituent": constituent}

    df = pd.DataFrame.from_dict(parse_info)
    return df


def get_paths(path_list, node, overarching_list):
    """
    Function that creates a constituency tree path for each word in text.
    """
    # check whether there is a syntax tree
    if path_list is None:
        return
    # if so, append current label
    path_list.append(node.label)
    # once you get to leaf, append path of the leaf
    if len(node.children) == 0:
        # exclude the leaf/word itself and add to overarching list
        overarching_list.append(path_list[:-1])
        # stop function
        return
    for n in node.children:
        # all children need to have same subpath, which is why .copy() is needed
        # keep getting paths until leaf is reached
        get_paths(path_list.copy(), n, overarching_list)


def run_pipeline(path_to_data):
    path_labels = []
    stanza_pipeline = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency')

    with open(path_to_data, encoding="utf-8") as f:
        for line in f.readlines():
            doc_stanza = stanza_pipeline(line)

            doc_sentences = list(doc_stanza.sentences)

            # for each sentence in the text, get the tree paths for the tokens in the sentence
            for i in range(len(doc_sentences)):
                get_paths([], doc_sentences[i].constituency.children[0], path_labels)

    print(path_labels)
    return path_labels


if __name__ == "__main__":
    data_path = "../data/article_with_eof_characters.txt"
    outfile = "../data/results_constituency_paths.tsv"

    df_structure = prepare_data(data_path)
    labels = run_pipeline(data_path)

    # exclude end of line characters
    df_structure = df_structure[df_structure["token"] != "\n"]

    # add new column to dataframe
    df_structure["paths"] = labels

    df_structure.to_csv("../data/full_constituents.csv")
