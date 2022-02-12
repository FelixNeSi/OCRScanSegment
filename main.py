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


def save_pages(images, root_file_name):
    for i, img in enumerate(images):
        img.save("{}-{}.png".format(i, root_file_name), "PNG")


def get_all_text_from_images(root_file_name, number_of_files):
    text = ''
    for i in range(number_of_files):
        temp_file_name = str(i) + root_file_name

        # im = Image.open(temp_file_name)
        # im = process_image_for_ocr(temp_file_name)

        image = cv2.imread(temp_file_name)
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


def convert_and_save_pdf_to_image(pdf_file_path, root_save_file_name, gray_scale=True):
    images = pdf_to_img(pdf_file_path, gray_scale=gray_scale)
    save_pages(images, root_save_file_name)

# img = Image.open("rotate_test.png")
# print(pytesseract.image_to_string(img, lang='eng'))

# TMP_regex = "([0-9]+|il|Ila|1S|DZ)(\.|,| )? ([A-Z][A-Z]+|[A-Z]\.)"
# all_text = get_all_text_from_images('-TMPimgGS.png', 141)
# do_segment_and_save(all_text, TMP_regex, "Taylor_Math_Practitioners.csv")

