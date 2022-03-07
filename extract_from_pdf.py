import re

import pandas as pd
from docx import *

####### VV CODE FOR MAIN SECTION OF MOLLAN VV #########

# document = Document('Mollan_Irish_National_Inventory_of_Historic_Scientific_Instruments_1995.docx')
# bolds = []
# bolds_info = {}
# found = False
# latest = '3950 ARM024 ALIDADE'
# for para in document.paragraphs:
#     # print('++++++++++++',para.text,'++++++++++++')
#     if found:
#         temp_bolds_info = bolds_info.get(latest, [])
#         temp_bolds_info.append(para.text)
#         bolds_info[latest] = temp_bolds_info
#     for run in para.runs:
#         # if run.italic and run.text != 'IRISH NATIONAL INVENTORY OF HISTORIC SCIENTIFIC INSTRUMENTS':
#         #     italics.append(run.text)
#         if run.bold and run.text != 'IRISH NATIONAL INVENTORY OF HISTORIC SCIENTIFIC INSTRUMENTS' and run.text != 'AURORA' and run.text != 'COULOMB':
#             temp_bolds_info = bolds_info.get(latest, [])
#             temp_bolds_info = temp_bolds_info[:-1]
#             bolds_info[latest] = temp_bolds_info
#
#             bolds.append(run.text)
#             found = True
#             counter = 0
#             latest = run.text
# #
#
# # boltalic_Dict={'bold_phrases':bolds}
# bolds = bolds[30:5199]
# print(bolds)
# # print(bolds_info['3985 ARM059 DIVIDED CIRCLE WITH REVOLVING DISC'])
# # print(bolds_info['3950 ARM024 ALIDADE'])
# # print(bolds_info['3707 ARM020 CHRONOGRAPH'])
# remove = ['CLONGOWES WOOD COLLEGE - CWC', 'Note: An overview of the collection, with some photographs, is given in ',
#           'The Clongownian', ' - see Mollan 1987.', "ST PATRICK'S COLLEGE, MAYNOOTH - MAY",
#           'Note: A comprehensive catalogue of the Maynooth instruments was',
#           'published in 1994, and this gives fuller descriptions of the instruments, with photographs; it also includes more 20th Century items - see bibliography under Mollan 1994.',
#           "NORTH MONASTERY CHRISTIAN BROTHERS' SCHOOL - NMC",
#           'Note: This collection was sold in 1993. Some of the key instruments were acquired by the National Museum in Dublin, and the remainder sold to a London dealer. Those transferred to the National Museum are included also in its listing in this Inventory, and Irish-signed instruments sold to London are included also in the Out-of-Ireland listing.',
#           'An overview of the collection is given Mollan 1993.', 'NATIONAL MUSEUM, DUBLIN - NMD',
#           'Note: During the period of the compiling of the National Inventory, '
#           'the collection at the National Museum has been dramatically increased and '
#           'improved, most notably by the acquisition of the collection of '
#           'instruments built up by Paul (who died in 1995) and Edith Egestorff. The '
#           'improvement in the collection has also been assisted through a scheme set '
#           'up by the Royal Dublin Society, by means of which commercial '
#           'organisations sponsored the purchase of important Irish instruments; by '
#           'the receipt of instruments from the collection of North Monastery School, '
#           'Cork; and by the purchase or donation of instruments discovered during '
#           'the Inventory work. The Egestorff acquisitions, the sponsored items, '
#           'and the "North Mon" instruments, are identified in the relevant '
#           'entries.', 'The collection is to be located in Collins Barracks, '
#                       'near the Phoenix Park.', 'Note: brackets around signatures in '
#                                                 'the above and later entries mean '
#                                                 'that the signatures have not been '
#                                                 'seen.', 'INSTRUMENTS RECORDED IN IRISH SALES - SAL',
#           'Note: The instruments in this section were seen in shops and in auction', 'sales.',
#           'Their whereabouts are now unknown.', 'UNIVERSITY COLLEGE GALWAY ENGINEERING - UGE',
#           'Note: This collection is particularly rich in instruments signed by the firm set up by Patrick Adie (1821-1886), the youngest son of Alexander Adie of Edinburgh.',
#           'Patrick worked in London from 1848 until his death, but instruments continued to be signed by the firm until 1942 - see Clifton 1995,4.',
#           'UNIVERSITY COLLEGE GALWAY GEOLOGY - UGG', 'INSTRUMENTS BY THE GRUBB FIRM OF DUBLIN']
# for r in remove:
#     bolds.remove(r)
#
#
# all_names, all_maker, all_dims, all_other = [], [], [], []
# for b in bolds:
#     print(b)
#     all_names.append(b)
#     current_info = bolds_info[b]
#     # print(current_info)
#     all_maker.append(current_info[0])
#     all_dims.append(current_info[1])
#     other_info = ''
#     for info in current_info[2:]:
#         other_info = other_info + info
#     all_other.append(other_info)
#
# df = pd.DataFrame(list(zip(all_names, all_maker, all_dims, all_other)),
#                   columns=['item name', 'item maker', 'dimensions/date', 'description'])
# df.to_csv("mollan_instruments.csv")


####### ^^ CODE FOR MAIN SECTION OF MOLLAN ^^ #########

document = Document('Mollan_Irish_National_Inventory_of_Historic_Scientific_Instruments_1995.docx')
paras = []
runs = []
for para in document.paragraphs:
    #print(para.text)
    paras.append(para.text)
    for run in para.runs:
        runs.append(run.text)
        # print(run.text)

print(paras.index('INDEX BY NAME OF MAKER OR SUPPLIER'))
paras = paras [47560:]
# print(paras)

print(runs.index('INDEX BY NAME OF MAKER OR SUPPLIER'))
runs = runs[35315:]
#print(runs)
no_page_numbers_runs = [run for run in paras if len(run)>3 and run != 'IRISH NATIONAL INVENTORY OF HISTORIC SCIENTIFIC INSTRUMENTS']

example = "Abdulla al-A'immah ASTROLABE 4524 CBL001 Abu-t-Tahir Muhammad ASTROLABE QUADRANT 4530 CBL007 AC COIL - INDUCTION, RUHMKORFF 0393 RDS076"
maker_name = []
other = []
for run in no_page_numbers_runs:
    # print(run)
    name_index = re.search(' ([A-Z]+/?-?(\(\?\))?)+ ', run).start()
    maker_name.append(run[:name_index])
    other.append(run[name_index:])

# for i in range(len(names)):
#     print(names[i], '++++++', other[i])

inventory_code = []
location_code = []
instrument_name = []

for oth in other:
    split_oth = oth.split()
    inventory_code.append(split_oth[-2])
    location_code.append(split_oth[-1])
    temp_instrument_name = ' '.join(split_oth[:-2])
    instrument_name.append(temp_instrument_name)

for i in range(len(maker_name)):
     print(maker_name[i], '++++++', instrument_name[i], '++++++', inventory_code[i], '++++++', location_code[i])

df = pd.DataFrame(list(zip(maker_name, instrument_name, inventory_code, location_code)),
                  columns=['maker name', 'instrument name', 'inventory code', 'location code'])
df.to_csv("mollan_index_by_name_of_maker.csv")

# regex = re.compile('\b[A-Z]+\b')
# testt = re.search(' [A-Z]+ ', run).start()
# # testt = regex.search("Abdulla al-A'immah ASTROLABE 4524 CBL001 Abu-t-Tahir Muhammad ASTROLABE QUADRANT 4530 CBL007 AC COIL - INDUCTION, RUHMKORFF 0393 RDS076").group(1)
# print(example[testt:])


# '3985 ARM059 DIVIDED CIRCLE WITH REVOLVING DISC'
# for para in document.paragraphs:
#     print('++++++++++++',para.text,'++++++++++++')
#     for run in para.runs:
#         # if run.italic and run.text != 'IRISH NATIONAL INVENTORY OF HISTORIC SCIENTIFIC INSTRUMENTS':
#         #     italics.append(run.text)
#         if run.bold and run.text != 'IRISH NATIONAL INVENTORY OF HISTORIC SCIENTIFIC INSTRUMENTS':
#             bolds.append(run.text)

# from PyPDF2 import PdfFileWriter, PdfFileReader
# input_pdf = PdfFileReader("Instruments of science.pdf")
# output = PdfFileWriter()
# for i in range(136):
#     output.addPage(input_pdf.getPage(i+400))
# with open("Instruments-of-science-400-end.pdf", "wb") as output_stream:
#     output.write(output_stream)
