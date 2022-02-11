import spacy
import pandas as pd

text_path = "../data/article.txt"
outfile = "../data/spacy_parse.tsv"

with open(text_path, encoding="utf-8") as f:
    content = f.read()

nlp = spacy.load("en_core_web_sm")
doc = nlp(content)

token = []
dependency = []
head = []
dependent = []
is_sent_start = []

for tok in doc:
    token.append(tok.text)
    dependency.append(tok.dep_)
    head.append(tok.head)
    dependent.append([t.text for t in tok.subtree if (t.text!=tok.text)])
    is_sent_start.append(tok.is_sent_start)

parse_info = {"token":token, "dependency":dependency, 
              "head":head, "dependent":dependent, 
              "is_sent_start":is_sent_start}
df = pd.DataFrame.from_dict(parse_info)
df.to_csv(path_or_buf=outfile, sep="\t", encoding="utf-8", index=False)
