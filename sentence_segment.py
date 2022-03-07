import spacy
import pandas as pd
from spacy.language import Language
from spacy.tokenizer import Tokenizer

# def create_pipeline(max_length=15000000):
#     disabled = ["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner"]
#
#     nlp = spacy.load("en_core_web_sm", disable=disabled)
#     nlp.max_length = max_length
#     nlp.add_pipe("sentencizer")
#
#     return nlp


def create_pipeline(lem=False, pos_tag=False, ner=False, added=None, max_length=15000000):
    # if disabled is None:
    #     disabled = ["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner"]
    disabled = ["tok2vec", "parser"]
    if not lem:
        disabled.append("lemmatizer")
        disabled.append("attribute_ruler")
    if not pos_tag:
        disabled.append("tagger")
    if not ner:
        disabled.append("ner")
    if added is None:
        added = ["sentencizer"]

    nlp = spacy.load("en_core_web_sm", disable=disabled)
    nlp.max_length = max_length
    for a in added:
        nlp.add_pipe(a)
    #print(nlp.pipeline)
    return nlp


def custom_tokenizer(nlp):
    return Tokenizer(nlp.vocab, rules=special_token_cases)


@Language.component("set_custom_boundaries")
def set_custom_boundaries(doc):
    for i, token in enumerate(doc):
        if token.text in taylor_custom_boundaries:
            doc[i].is_sent_start = False
    return doc


def create_custom_pipeline():
    nlp = create_pipeline()
    # nlp.tokenizer = custom_tokenizer(nlp)
    for case in special_token_cases:
        nlp.tokenizer.add_special_case(case, [{"ORTH": case}])
    # nlp.tokenizer.add_special_case("(viz.)", [{"ORTH": "(viz.)"}])
    # {"(viz.)", [{"ORTH": "(viz.)"}]}
    nlp.add_pipe("set_custom_boundaries", before="sentencizer")
    return nlp


def split_doc_sentences(nlp, text, entry_number):
    doc = nlp(text)
    entry_numbers, sentences, sentence_numbers = [], [], []
    for j, sent in enumerate(doc.sents):
        sentences.append(' '.join(sent.text.split()))
        entry_numbers.append(entry_number)
        sentence_numbers.append(j)
    return sentences[:-1], entry_numbers[:-1], sentence_numbers[:-1]


def split_all_sentences(texts, entry_numbers):
    # nlp = create_pipeline()
    nlp = create_custom_pipeline()
    all_sentences, all_entry_numbers, all_sentence_numbers = [], [], []
    for i, text in enumerate(texts):
        temp_sentences, temp_entry_numbers, temp_sentence_numbers = split_doc_sentences(nlp, text, entry_numbers[i])
        all_sentences = all_sentences + temp_sentences
        all_entry_numbers = all_entry_numbers + temp_entry_numbers
        all_sentence_numbers = all_sentence_numbers + temp_sentence_numbers
    return all_sentences, all_entry_numbers, all_sentence_numbers


def do_split_and_save(file_path, save_file_name, header=["entry_sentence", "entry_number", "sentence_number"]):
    df_to_split = pd.read_csv(file_path)
    entries = df_to_split['entry'].tolist()
    ids = df_to_split['pract_id'].tolist()
    all_sents, all_ids, all_sentence_numbers = split_all_sentences(entries, ids)

    df_to_save = pd.DataFrame(list(zip(all_sents, all_ids, all_sentence_numbers)))
    df_to_save.to_csv(save_file_name, index=False, header=header)


taylor_custom_boundaries = (
'ive.', 'fi.', 'fl.', 'ob.', '(tt.', 'I(fi.', 'll.', '11a.', '?),', 'fil.', 'cire.', 'etc.,', 'circ.', 'esq.', '47a.',
'ic.', 'ft.', 'i.c.', '6d.', 'philomath.', 'gent.,', '..', '.. . . ', '(?')
special_token_cases = {'ive.': [{"ORTH": 'ive.'}], 'fi.': [{"ORTH": 'fi.'}], 'fl.': [{"ORTH": 'fl.'}], 'ob.': [{"ORTH": 'ob.'}], '(tt.': [{"ORTH": '(tt.'}], 'I(fi.': [{"ORTH": 'I(fi.'}], 'll.': [{"ORTH": 'll.'}], '11a.': [{"ORTH": '11a.'}], '?),': [{"ORTH": '?),'}], 'fil.': [{"ORTH": 'fil.'}], 'cire.': [{"ORTH": 'cire.'}], 'etc.,': [{"ORTH": 'etc.,'}], 'circ.': [{"ORTH": 'circ.'}], 'esq.': [{"ORTH": 'esq.'}], '47a.': [{"ORTH": '47a.'}], 'ic.': [{"ORTH": 'ic.'}], 'ft.': [{"ORTH": 'ft.'}], 'i.c.': [{"ORTH": 'i.c.'}], '6d.': [{"ORTH": '6d.'}], 'philomath.': [{"ORTH": 'philomath.'}], 'gent.,': [{"ORTH": 'gent.,'}], '..': [{"ORTH": '..'}], '.. . . ': [{"ORTH": '.. . . '}], '(?': [{"ORTH": '(?'}]}
do_split_and_save("3_Taylor_Math_Practitioners.csv", "1_Sentences_Taylor_Math_Practitioners.csv")




# s=''
# for t in taylor_custom_boundaries:
#     # print("'{}': [{"'{}'": '{}'}]".format(t,'ORTH', t))
#     s = s +  "'"+t+"': [{"+'"ORTH": '+"'"+t+"'}], "
#     #print("'"+t+"': [{"+'"ORTH": '+"'"+t+"'}], ")

# print(s)
