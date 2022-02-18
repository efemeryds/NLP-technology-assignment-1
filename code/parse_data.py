import spacy
import pandas as pd

text_path = "../data/article.txt"
outfile = "../results/spacy_parse.tsv"

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
#is_sent_start = [tok.is_sent_start for tok in doc]

parse_info = {"token": token, "dependency": dependency,
              "head": head, "dependent": dependent,
              "constituent": constituent}
              #"is_sent_start":is_sent_start}
df = pd.DataFrame.from_dict(parse_info)
df.to_csv(path_or_buf=outfile, sep="\t", encoding="utf-8", index=False)
