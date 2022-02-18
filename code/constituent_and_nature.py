import pandas as pd
from typing import List


def read_parse_result(parse_path: str):
    return pd.read_csv(parse_path, sep="\t", quotechar="|", encoding="utf-8")


def extract_constituent_of_head(dataframe) -> List[str]:
    constituent_of_head = []
    for i in range(dataframe.shape[0]):
        target = dataframe.iloc[i]  # For each target word
        if target["dependent"] == "[]":  # If no dependents -> not head word
            constituent_of_head.append("NOT_HEAD")
        else:
            constituent_of_head.append(target["constituent"])  # If head -> append constituent
    return constituent_of_head


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


def write_features(dataframe, outfile):
    dataframe.to_csv(path_or_buf=outfile, sep="\t", encoding="utf-8")


if __name__ == "__main__":
    parse = read_parse_result("../results/spacy_parse.tsv")
    constituent_of_head = extract_constituent_of_head(parse)
    nature = extract_nature_of_dep(parse)

    features_df = pd.DataFrame({"token": parse["token"],
                                "constituent_of_head": constituent_of_head,
                                "nature": nature})

    outfile = "../results/features.tsv"
    write_features(features_df, outfile)
