import spacy
import pandas as pd

def create_pipeline(max_length=15000000):
    disabled = ["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner"]

    nlp = spacy.load("en_core_web_sm", disable=disabled)
    nlp.max_length = max_length
    nlp.add_pipe("sentencizer")

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
    nlp = create_pipeline()
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


do_split_and_save("3_Taylor_Math_Practitioners.csv", "1_Sentences_Taylor_Math_Practitioners.csv")
