# NLP Technology syntax assignment 
Solutions for the Syntax part of the assignment

## AUTHORS
------------------
A.M. Dobrzeniecka (Alicja), E.H.W. Galjaard (Ellemijn), T.A. Wisman (Tessel), Y.C. Li (Roderick)

## PROJECT STRUCTURE
-------------------
```
├── code 
│   ├── extract_head_of_target.py 
│   ├── extract_sentence_features.ipynb
│   ├── extract_token_features.py
│   ├── parse_data.py            
├── data    
│   ├── article.txt   
│   ├── article_with_eof_characters.txt           
├── results 
│   ├── sentence_features.csv   
│   ├── spacy_parse.tsv           
│   ├── token_features.csv
```

## IMPLEMENTED FEATURES
Token level:
- Nature of dependency
- Head
- Number of dependents
- Constituent of head
- Constituency path (from S to POS-tag of token)
- Head of target (sample)

Sentence level:
- Full syntactic tree
- Dependency path

## HOW TO USE IT
- STEP 1. Install libraries specified in **requirements.txt** by running "pip install -r requirements.txt"
- STEP 2. Run `parse_data.py` in **code/** to parse **data/article.txt** 
- STEP 3. Run `extract_*.py` in **code/** to get features from **data/article.txt** 
- STEP 4. Check the results in **results/**

## REMARKS 

- the text in 'article.txt' is obtained from NL Times (https://nltimes.nl/2022/02/09/sources-netherlands-abolish-covid-rules-beginning-march, viewed on 10 Feb). All rights reserved

- extract_head_of_target.py is an experimental file where one can get a head of the target word for manually defined sentence and target word


