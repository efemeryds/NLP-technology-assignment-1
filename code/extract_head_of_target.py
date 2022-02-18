import stanza


def read_file(path):
    with open(path, 'r') as infile:
        text = infile.readlines()
    # print(''.join(text))
    return text


def parse_doc(text):
    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
    text = text.lower()
    doc = nlp(text)
    # from the Stanford doc: https://stanfordnlp.github.io/stanza/depparse.html
    # print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')
    return doc


def extract_target(target, parsed_sentence):
    ''' extracts target word in parsed sentence 
    param: target: the target word (str)
    param: parsed_sentenced: a stanza doc object of the parsed sentence 
    returns: target_in_doc: the stanza word object corresponding to the target'''
    target_in_doc = []
    for doc_el in parsed_sentence.words:  # go through sentence
        if doc_el.text == target:
            target_in_doc.append(doc_el)
    if len(target_in_doc) <= 0:
        print('element not found')
        return False
    return target_in_doc


def get_head_of_targetword(target, sentence):
    '''
    param: target: the target word (str)
    param: sentence: the sentence containing the target word
    returns: target_head: the head of the target word '''
    # parsed_sentence = parse_doc(sentence)
    target_in_doc = extract_target(target, sentence)
    for target_elem in target_in_doc:
        head_id = target_elem.head
        target_head = sentence.words[head_id - 1].text if head_id > 0 else "root"
        print('head of', target, ':\t', target_head)
        return target_head


testfile = read_file('..\parsetest_ams.txt')
print(''.join(testfile))
doc = parse_doc(''.join(testfile))
get_head_of_targetword('some', doc.sentences[0])
