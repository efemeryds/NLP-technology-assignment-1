import nltk
import pandas as pd
import stanza
# stanza.download('en')

sub_labels = []

with open("../data/article.txt", encoding="utf-8") as f:
    content = f.read()

nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency')


def syntax(text_list):
    df_list = []
    for sentence in text_list:
        doc = nlp(sentence)
        const = doc.sentences[0].constituency
        df_list.append({"sentence": sentence, "const": const})

    final_df = pd.DataFrame(df_list)
    return final_df


if __name__ == "__main__":

    with open("../data/article.txt", encoding="utf-8") as f:
        content = f.read()

    # convert text into a list of sentences
    text_list_input = nltk.tokenize.sent_tokenize(content)
    const = syntax(text_list_input)
    const.to_csv("../results/full_tree.csv")
    print('DONE')

