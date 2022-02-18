# NLP-technology-assignment-1
Solutions for the Syntax part of the assignment

## AUTHORS
------------------
A.M. Dobrzeniecka (Alicja), E.H.W. Galjaard (Ellemijn), T.A. Wisman (Tessel), Y.C. Li (Roderick)


## TABLE OF CONTENTS
-------------------
```
├── code 
│   ├── full_constituency_paths.py 
│   ├── constituency_paths.ipynb
│   ├── extract_constituent_and_nature.py
│   ├── parse.py  # 'parse.py' contains code to parse a text from the `../data` folder to get syntactic features with spaCy. Results are also saved in this folder. 
│   ├── shortest_dependency_path.py
│   └── stanza_const.py            
├── data    # This folder stores the original text to be parsed ('article.txt') and the results of parsing ('spacy_parse.tsv').  
│   ├── article.txt   
│   ├── article_with_eof_characters.txt           
│   ├── constituency.csv
│   ├── features.tsv
│   ├── shortest_path.csv
│   └── spacy_parse.tsv
```


The text in 'article.txt' is obtained from NL Times (https://nltimes.nl/2022/02/09/sources-netherlands-abolish-covid-rules-beginning-march, viewed on 10 Feb). All rights reserved.  



## COMMENTS

In full_constituency_paths.py the resulting full_constituents.csv file contains sometimes in the path double "S", it comes from the Stanza parser therefore we did not change it or undermine it in any way. 


