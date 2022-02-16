import os

import pdf2image
from PIL import Image
import pytesseract
import re
from pdfImagePreprocessing import process_image_for_ocr, correct_skew
import pandas as pd
import cv2


def pdf_to_img(pdf_file, dpi=300, gray_scale=False):
    return pdf2image.convert_from_path(pdf_file, dpi=dpi, grayscale=gray_scale)


def ocr_core(file):
    text = pytesseract.image_to_string(file)
    return text


def print_pages(pdf_file):
    images = pdf_to_img(pdf_file)
    save_pages(images, "TMPimg")
    for pg, img in enumerate(images[:3]):
        # print(ocr_core(img))
        text = ocr_core(img)
        nlines = text.replace('\n\n', "**NEWLINES**")
        print(nlines)
        # print("NEW LINES: ", str(nlines))


def save_pages(images, root_file_name, name_offset=0):
    for i, img in enumerate(images):
        img.save("{}-{}.png".format(str(i + name_offset), root_file_name), "PNG")


def get_all_text_from_images(root_file_name, number_of_files):
    text = ''
    for i in range(number_of_files):
        #temp_file_name = str(i) + root_file_name
        temp_file_name = "sci-preserved-{}.jpg".format((str(i+1)))
        # im = Image.open(temp_file_name)
        # im = process_image_for_ocr(temp_file_name)

        image = cv2.imread(temp_file_name)
        print("Attempting file: ", temp_file_name)
        angle, im = correct_skew(image)

        text = text + " " + pytesseract.image_to_string(im, lang='eng')
    return text


def regex_segment(text, regex_pattern):
    regex = re.compile(regex_pattern, re.DOTALL)
    segmented_text_indices = [(m.start(0), m.end(0)) for m in re.finditer(regex, text)]
    segmented_text = []
    prev = 0
    for i in segmented_text_indices[1:]:
        segmented_text.append(text[prev:i[0]])
        prev = i[0]
    segmented_text.append(text[prev:])
    return segmented_text


def do_segment_and_save(text, regex_pattern, file_name):
    segmented_text = regex_segment(text, regex_pattern)
    df = pd.DataFrame(segmented_text)
    df.to_csv(file_name)


def convert_and_save_pdf_to_image(pdf_file_path, root_save_file_name, name_offset=0, gray_scale=True):
    images = pdf_to_img(pdf_file_path, gray_scale=gray_scale)
    save_pages(images, root_save_file_name)


def extract_id_numbers(entry_list, split_char='.'):
    id_numbers = [entry.split(split_char)[0] for entry in entry_list]
    return id_numbers


def join_save_df(save_name, col1, col2, col3, header=["pract_id", "entry", "work_ids"]):
    df = pd.DataFrame(list(zip(col1, col2, col3)))
    df.to_csv(save_name, index=False, header=header)


def do_extract_entry_id(file_name, save_file_name):
    df = pd.read_csv(file_name, index_col=False)
    x = df['0'].tolist()
    ids = extract_id_numbers(x)
    join_save_df(save_file_name, ids, x)


def extract_work_ids(file_name, save_file_name):
    df = pd.read_csv(file_name)
    work_ids = []
    entries = df['entry'].tolist()
    ids = df['pract_id'].tolist()
    for e in entries:
        work = re.search('(work:|Work:|works:|Works:)', e)
        if work is None:
            work_ids.append("")
        else:
            temp_id = e[work.span()[1]:].replace(".", "")
            temp_id = temp_id.replace("/", "1")
            temp_id = temp_id.replace("J", "1")
            work_ids.append(temp_id)
        # print(works.span()[1])
        # index = works.span()[1]
        # print(x0[index:])
    join_save_df(save_file_name, ids, entries, work_ids)


# img = Image.open("rotate_test.png")
# print(pytesseract.image_to_string(img, lang='eng'))

# TMP_regex = "([0-9]+|il|Ila|1S|DZ)(\.|,| )? ([A-Z][A-Z]+|[A-Z]\.)"
# work_regex = "([0-9]+|il|Ila|1S|DZ)(\.|,| )? ([A-Z][A-Z]+|[A-Z]\.)"
#


for i in range(213):
    # temp_file_name = str(i) + root_file_name
    temp_file_name = "sci-preserved-{}.jpg".format((str(i + 1)))
    image = cv2.imread(temp_file_name)
    # image = Image.open(temp_file_name)
    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    new_file_name = "{}-sci-preserved.png".format((str(i + 1)))
    cv2.imwrite(new_file_name, img_grey)

# all_text = get_all_text_from_images('-EGRT_work.png', 1)
# print(all_text)
# do_segment_and_save(all_text, work_regex, "Taylor_Works.csv")

# convert_and_save_pdf_to_image("EGRT Works II.pdf", "EGRT_works", 24)

# img = Image.open("1-EGRT_works.png")
# img.save("00.png", "PNG")

# names = os.listdir("Scans")
# print(names[0][18:26])
