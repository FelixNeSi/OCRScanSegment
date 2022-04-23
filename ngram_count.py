from nltk.util import ngrams
import pandas as pd


def count_freq(ngram_list):
    gram_freq = {}
    for gram in ngram_list:
        for g in gram:
            temp = gram_freq.get(g, 0)
            temp += 1
            gram_freq[g] = temp
    return gram_freq


def reformat_ngram_count(ngram_dict, ngram_count):
    all_words = []
    all_freq = []

    for i in range(ngram_count):
        all_words.append([])

    for k, v in ngram_dict.items():
        # temp = ""
        for i, w in enumerate(k):
            all_words[i].append(k[i])
        #     temp = '{} {}'.format(temp, w)
        # all_words.append(temp)
        all_freq.append(v)
    return all_words, all_freq


def do_count_and_save_ngrams(original_file_name, save_file_name, text_column_header="Text"):
    o_df = pd.read_csv(original_file_name)
    text = o_df[text_column_header].tolist()

    uni_grams = [ngrams(txt.split(), 1) for txt in text if not isinstance(txt, float)]
    bi_grams = [ngrams(txt.split(), 2) for txt in text if not isinstance(txt, float)]
    tri_gram = [ngrams(txt.split(), 3) for txt in text if not isinstance(txt, float)]
    four_gram = [ngrams(txt.split(), 4) for txt in text if not isinstance(txt, float)]
    five_gram = [ngrams(txt.split(), 5) for txt in text if not isinstance(txt, float)]

    all_uni_grams = count_freq(uni_grams)
    all_uni_grams = {k: v for k, v in sorted(all_uni_grams.items(), key=lambda item: item[1], reverse=True)}
    all_bi_grams = count_freq(bi_grams)
    all_bi_grams = {k: v for k, v in sorted(all_bi_grams.items(), key=lambda item: item[1], reverse=True)}
    all_tri_gram = count_freq(tri_gram)
    all_tri_gram = {k: v for k, v in sorted(all_tri_gram.items(), key=lambda item: item[1], reverse=True)}
    all_four_gram = count_freq(four_gram)
    all_four_gram = {k: v for k, v in sorted(all_four_gram.items(), key=lambda item: item[1], reverse=True)}
    all_five_gram = count_freq(five_gram)
    all_five_gram = {k: v for k, v in sorted(all_five_gram.items(), key=lambda item: item[1], reverse=True)}
    re_uni, uni_freq = reformat_ngram_count(all_uni_grams, 1)
    re_bi, bi_freq = reformat_ngram_count(all_bi_grams, 2)
    re_tri, tri_freq = reformat_ngram_count(all_tri_gram, 3)
    re_four, four_freq = reformat_ngram_count(all_four_gram, 4)
    re_five, five_freq = reformat_ngram_count(all_five_gram, 5)

    df1 = pd.DataFrame(list(zip(re_uni[0], uni_freq)))
    df1.to_csv("{}_unigram_freq.csv".format(save_file_name), header=["word-1", "freq"])
    #
    # df2 = pd.DataFrame(list(zip(re_bi, bi_freq)))
    df2 = pd.DataFrame(list(zip(re_bi[0], re_bi[1], bi_freq)))
    df2.to_csv("{}_bigram_freq.csv".format(save_file_name), header=["word-1", "word-2", "freq"])
    #
    df3 = pd.DataFrame(list(zip(re_tri[0], re_tri[1], re_tri[2], tri_freq)))
    df3.to_csv("{}_trigram_freq.csv".format(save_file_name), header=["word-1", "word-2", "word-3", "freq"])

    df4 = pd.DataFrame(list(zip(re_four[0], re_four[1], re_four[2], re_four[3], four_freq)))
    df4.to_csv("{}_four_gram_freq.csv".format(save_file_name), header=["word-1", "word-2", "word-3", "word-4", "freq"])

    df5 = pd.DataFrame(list(zip(re_five[0], re_five[1], re_five[2], re_five[3], re_five[4], five_freq)))
    df5.to_csv("{}_five_gram_freq.csv".format(save_file_name),
               header=["word-1", "word-2", "word-3", "word-4", "word-5", "freq"])

    df6 = pd.concat([df1, df2, df3, df4, df5], axis=1)
    df6.columns = ["word-1", "freq", "word-1", "word-2", "freq", "word-1", "word-2", "word-3", "freq", "word-1",
                   "word-2", "word-3", "word-4", "freq", "word-1", "word-2", "word-3", "word-4", "word-5", "freq"]
    df6.to_csv("{}_all_gram_freq.csv".format(save_file_name))


# Example of how to use the function, FIRST parameter is the original file name to count ngrams from SECOND parameter
# is the the root for the file name to save, e.g. 'dramatis' as parameter will create file names such as-
# -'dramatis_bigram_freq.csv' and 'dramatis_all_gram_freq.csv'
# THIRD parameter is the column header for which the text resides that you want to count e.g.
# 'additional info' in terms of the 'dramatis personae' csv
do_count_and_save_ngrams("dramatis personae v7.csv", "dramatis", "additional info")
