import numpy as np
import pandas as pd
import re
from main import regex_segment
#
# df = pd.read_csv("1mollan_instruments.csv")
# date_and_dims = df[dimensions/date].tolist()
#
# print(date_and_dims)
#
# dates = []
# dims = []
#
# for datedim in date_and_dims:
#     inde = datedim.find(.)
#     dims.append(datedim[:inde])
#     temp_date = datedim[inde:]
#     if temp_date[0] == ".":
#         dates.append(datedim[inde+1:])
#     else:
#         dates.append(datedim[inde:])
#
#
# df.drop(columns=[dimensions/date])
# df.insert(3, "dates", dates, allow_duplicates=True)
# df.insert(4, "dimensions", dims, allow_duplicates=True)
#
# df.to_csv("2-Mollan-Instruments.csv")

# df = pd.read_csv("2022-03-15-dramatis-personae fixed.csv")

# names = df['name'].tolist()
# simon_maker = df['simon_maker'].tolist()
#
# regex_pattern = '(, [a-z]|1[0-9][0-9][0-9]|\*|\(| f |bap\.|bap|B\.c|b\.c\.| c\.| b\.|Fp|S_|s_|m\.|m_|Present|Nd|Decd\.|d\.|As|By|Whose|His|In|For|Who|Daughter|Mrs|CKC|SMC|STC|as, |of, |in, |at, |by |to |as |was |before | b | m | of |\[)'
#
# new_info = []
# new_names = []
# agents = []
# suppliers = []
# df.fillna("")
#
# agent_supp_list = ['agent', 'supplier', 'supplied', 'supply']
# for i in range(len(names)):
#     if not isinstance(names[i], float):
#         if 'agent' in names[i].lower():
#             agents.append("TRUE")
#         else:
#             agents.append("FALSE")
#         if 'supplier' in names[i].lower() or 'supplied' in names[i].lower() or 'supply' in names[i].lower():
#             suppliers.append("TRUE")
#         else:
#             suppliers.append("FALSE")
#     else:
#         agents.append("FALSE")
#         suppliers.append("FALSE")
#     if not simon_maker[i] and not isinstance(names[i], float):
#         temp = re.split(regex_pattern, names[i])
#         print(names[i], " +++ ", simon_maker[i])
#         print(names[i], " +++ ", temp)
#         new_names.append(temp[0])
#         temp_info = ''.join(temp[1:])
#         new_info.append(temp_info)
#     else:
#         new_names.append(names[i])
#         new_info.append("")
#
# df = df.drop(columns=['name'])
# df.insert(2, "name", new_names, allow_duplicates=True)
# df.insert(3, "additional info", new_info, allow_duplicates=True)
# df.insert(4, "agent", agents, allow_duplicates=True)
# df.insert(5, "supplier", suppliers, allow_duplicates=True)
#
# df.to_csv("dramatis personae v7.csv", index=False)

# df = pd.read_csv("dramatis personae v7.csv")
#
# add_info = df['additional info'].tolist()
#
# new_prev, new_post = [], []
#
#
# for inf in add_info:
#     if not isinstance(inf, float):
#         temp_inf = inf.split(" of", 1)
#         new_prev.append(temp_inf[0])
#         new_temp = ' '.join(temp_inf[1:])
#         new_post.append(new_temp)
#     else:
#         new_prev.append('')
#         new_post.append('')
#
# df = df.drop(columns=['additional info'])
# df.insert(4, "additional_info", new_prev, allow_duplicates=True)
# df.insert(5, "post 'of'", new_post, allow_duplicates=True)
# df.to_csv("dramatis personae v8.csv", index=False)

from nltk.util import ngrams
o_df = pd.read_csv("dramatis personae v7.csv")
text = o_df['additional info'].tolist()

uni_grams = [ngrams(txt.split(), 1) for txt in text if not isinstance(txt, float)]
bi_grams = [ngrams(txt.split(), 2) for txt in text if not isinstance(txt, float)]
tri_gram = [ngrams(txt.split(), 3) for txt in text if not isinstance(txt, float)]
four_gram = [ngrams(txt.split(), 4) for txt in text if not isinstance(txt, float)]
five_gram = [ngrams(txt.split(), 5) for txt in text if not isinstance(txt, float)]


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
df1.to_csv("unigram_freq.csv", header=["word-1", "freq"])
#
# df2 = pd.DataFrame(list(zip(re_bi, bi_freq)))
df2 = pd.DataFrame(list(zip(re_bi[0], re_bi[1] , bi_freq)))
df2.to_csv("bigram_freq.csv", header=["word-1", "word-2", "freq"])
#
df3 = pd.DataFrame(list(zip(re_tri[0], re_tri[1], re_tri[2], tri_freq)))
df3.to_csv("trigram_freq.csv", header=["word-1", "word-2", "word-3", "freq"])

df4 = pd.DataFrame(list(zip(re_four[0], re_four[1], re_four[2], re_four[3], four_freq)))
df4.to_csv("four_gram_freq.csv", header=["word-1", "word-2", "word-3", "word-4", "freq"])

df5 = pd.DataFrame(list(zip(re_five[0], re_five[1], re_five[2], re_five[3], re_five[4], five_freq)))
df5.to_csv("five_gram_freq.csv", header=["word-1", "word-2", "word-3", "word-4", "word-5", "freq"])

df6 = pd.concat([df1, df2, df3, df4, df5], axis=1)
df6.columns = ["word-1", "freq", "word-1", "word-2", "freq", "word-1", "word-2", "word-3", "freq", "word-1", "word-2", "word-3", "word-4", "freq", "word-1", "word-2", "word-3", "word-4", "word-5", "freq"]
df6.to_csv("all_gram_freq.csv")
#
# mega_df = pd.DataFrame(list(zip(re_uni, uni_freq, re_bi, bi_freq, re_tri, tri_freq, re_four, four_freq, re_five, five_freq)))
# mega_df.to_csv("all_gram_freq.csv", header=["unigram", "uni_freq", "bigram", "bi_freq", "trigram", "tri_freq", "fourgram", "four_freq", "fivegram", "five_freq"])
# for gram in uni_grams:
#       for g in gram:
#             temp = all_uni_grams.get(g, 0)
#             temp += 1
#             all_uni_grams[g] = temp
#
# for gram in bi_grams:
#       for g in gram:
#             temp = all_bi_grams.get(g, 0)
#             temp += 1
#             all_bi_grams[g] = temp
#
# for gram in tri_gram:
#       for g in gram:
#             temp = all_tri_gram.get(g, 0)
#             temp += 1
#             all_tri_gram[g] = temp
#
# for gram in four_gram:
#       for g in gram:
#             temp = all_four_gram.get(g, 0)
#             temp += 1
#             all_four_gram[g] = temp
#
# for gram in five_gram:
#       for g in gram:
#             temp = all_five_gram.get(g, 0)
#             temp += 1
#             all_five_gram[g] = temp

# for k, v in all_uni_grams.items():
#       print('{} := {}'.format(k, v))
#
# for k, v in all_tri_gram.items():
#       print('{} := {}'.format(k, v))
