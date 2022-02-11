import pdf2image
from PIL import Image
import pytesseract
import re
from pdfImagePreprocessing import process_image_for_ocr
import pandas as pd


def pdf_to_img(pdf_file):
    return pdf2image.convert_from_path(pdf_file)


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


def save_pages(images, root_file_name):
    for i, img in enumerate(images):
        img.save("{}-{}.png".format(i, root_file_name), "PNG")


def get_all_text_from_images(root_file_name, number_of_files):
    text = ''
    for i in range(number_of_files):
        temp_file_name = str(i+1) + root_file_name
        im = Image.open(temp_file_name)
        # im = process_image_for_ocr(temp_file_name)
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


def convert_and_save_pdf_to_image(pdf_file_path, root_save_file_name):
    images = pdf_to_img(pdf_file_path)
    save_pages(images, root_save_file_name)


# all_text = get_all_text_from_images('-TMPimg.png', 141)
#
# myre = re.compile("([0-9]+|il|Ila|1S|DZ)(\.|,| )? ([A-Z][A-Z]+|[A-Z]\.)", re.DOTALL)
# # print(re.findall(myre, text))
#
# x = [(m.start(0), m.end(0)) for m in re.finditer(myre, all_text)]
# segmented_x = []
# prev = 0;
# for i in x[1:]:
#     segmented_x.append(all_text[prev:i[0]])
#     prev = i[0]
# segmented_x.append(all_text[prev:])
# # for s in segmented_x:
# #     print('**********' + s)
#
# df = pd.DataFrame(segmented_x)
# df.to_csv("test_seg2.csv")
