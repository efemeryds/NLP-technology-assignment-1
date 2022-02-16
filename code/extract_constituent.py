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


def write_features(dataframe, outfile):
    dataframe.to_csv(path_or_buf=outfile, sep="\t", encoding="utf-8")


parse = read_parse_result("../data/spacy_parse.tsv")
constituent_of_head = extract_constituent_of_head(parse)

features_df = pd.DataFrame({"token": parse["token"],
                            "constituent_of_head": constituent_of_head})

outfile = "../data/features.tsv"
write_features(features_df, outfile)
