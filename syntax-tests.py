import stanza

def read_file(path):
    with open(path, 'r') as infile:
        text = infile.readlines()
    #print(''.join(text))    
    return text

def parse_doc(text):
    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
    text = text.lower()
    doc = nlp(text)
    # from the Stanford doc: https://stanfordnlp.github.io/stanza/depparse.html
    #print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')
    return doc

def extract_target(target, parsed_sentence):
    target_in_doc = []
    for doc_el in parsed_sentence.words:
        if doc_el.text == target:
            target_in_doc.append(doc_el)
    if len(target_in_doc) <=0:
        print('element not found')
        return False
    return target_in_doc 

def get_head_of_targetword(target, sentence):
    #parsed_sentence = parse_doc(sentence)
    target_in_doc = extract_target(target, sentence)
    for target_elem in target_in_doc:
        head_id = target_elem.head
        target_head = sentence.words[head_id-1].text if head_id > 0 else "root"
        print(target, 'head:', target_head)

testfile = read_file('..\parsetest_ams.txt')
print(''.join(testfile))
doc = parse_doc(''.join(testfile))
get_head_of_targetword('universities', doc.sentences[0])