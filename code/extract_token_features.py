import spacy
import pandas as pd
import stanza
from typing import List


# run in terminal, if you don't have the package: python3 -m spacy download en_core_web_sm

def read_parse_result(parse_path: str):
    return pd.read_csv(parse_path, sep="\t", quotechar="|", encoding="utf-8")


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


def extract_nature_of_dep(dataframe) -> List[str]:
    mods = {"acl", "advcl", "amod", "appos", "compound",
            "meta", "nounmod", "npmod", "nummod", "poss", "quantmod", "relcl"}
    tuns = {"advmod"}
    inv = {"neg"}
    preps = {"prep"}
    verbs = {"ROOT", "ccomp", "csubj", "csubjpass", "pcomp", "xcomp"}
    nature = []
    for i in range(dataframe.shape[0]):
        target = dataframe.iloc[i]  # For each target word
        if target["dependency"] in mods:  # If it is one of the modifiers,...
            nature.append("MOD")  # ...its nature is MODS, etc.
        elif target["dependency"] in tuns:
            nature.append("TUN")
        elif target["dependency"] in inv:
            nature.append("INV")
        elif target["dependency"] in preps:
            nature.append("PREP")
        elif target["dependency"] in verbs:
            nature.append("VERB")
        else:
            nature.append("OTH")
    return nature


def extract_head(dataframe) -> List[str]:
    return dataframe["head"].to_list()


def count_dependents(dataframe) -> List[str]:
    nr_of_dependents = []
    for i in range(dataframe.shape[0]):
        target = dataframe.iloc[i]  # For each target word
        if target["dependent"] == "[]":  # Check if there are dependents
            nr_of_dependents.append(int(0))
        else:
            nr_of_items = (target["dependent"].count("'"))//2  # One item has two "'"s
            nr_of_dependents.append(int(nr_of_items))
    return nr_of_dependents


def extract_constituent_of_head(dataframe) -> List[str]:
    constituent_of_head = []
    for i in range(dataframe.shape[0]):
        target = dataframe.iloc[i]  # For each target word
        if target["dependent"] == "[]":  # If no dependents -> not head word
            constituent_of_head.append("NOT_HEAD")
        else:
            constituent_of_head.append(target["constituent"])  # If head -> append constituent
    return constituent_of_head


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
    outfile = "../results/results_constituency_paths.tsv"

    # extract features
    parse = read_parse_result("../results/spacy_parse.tsv")
    nature = extract_nature_of_dep(parse)
    head = extract_head(parse)
    nr_of_dep = count_dependents(parse)
    constituent_of_head = extract_constituent_of_head(parse)

    df_structure = prepare_data(data_path)
    labels = run_pipeline(data_path)

    # exclude end of line characters
    df_structure = df_structure[df_structure["token"] != "\n"]
    df_structure_2 = pd.DataFrame(df_structure["token"])

    # add new columns to dataframe
    df_structure_2["nature"] = nature
    df_structure_2["head"] = head
    df_structure_2["nr_of_dependents"] = nr_of_dep
    df_structure_2["constituent_of_head"] = constituent_of_head
    df_structure_2["constituency_paths"] = labels

    df_structure_2.to_csv("../results/token_features.csv")
