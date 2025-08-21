from functools import cache
from multiprocessing import Pool, cpu_count
from tempfile import NamedTemporaryFile

import pytesseract
from pdf2image import convert_from_path
from pytesseract import Output
from utils import Log

from utils_future.pdf_file.PDFCompress import PDFCompress

TESSERACT_FAST_CONFIG = r"""
--oem 1
--psm 6
"""

log = Log("PDFImageText")


class PDFImageText:
    @staticmethod
    def __get_image_block_info_list_for_page__(i_page, im):
        temp_img_path = NamedTemporaryFile(suffix=".png", delete=False).name
        im.save(temp_img_path, format="PNG")

        data = pytesseract.image_to_data(
            temp_img_path,
            lang="eng",
            config=TESSERACT_FAST_CONFIG,
            output_type=Output.DICT,
        )
        list_for_page = []
        for i, text in enumerate(data["text"]):
            p_confidence = data["conf"][i] / 100.0
            datum = dict(
                i_page=i_page,
                level=data["level"][i],
                text=text,
                page_num=data["page_num"][i],
                par_num=data["par_num"][i],
                block_num=data["block_num"][i],
                line_num=data["line_num"][i],
                word_num=data["word_num"][i],
                bbox=[
                    round(x, 2)
                    for x in (
                        data["left"][i],
                        data["top"][i],
                        data["width"][i],
                        data["height"][i],
                    )
                ],
                p_confidence=p_confidence,
            )

            list_for_page.append(datum)

        group_by_par = {}
        for datum in list_for_page:
            par_num = datum["par_num"]
            if par_num not in group_by_par:
                group_by_par[par_num] = []
            group_by_par[par_num].append(datum)

        list_for_page_by_par = []
        for par_num, data_for_par in group_by_par.items():
            datum = dict(
                i_page=i_page,
                par_num=par_num,
                text=" ".join(datum["text"] for datum in data_for_par),
                mean_p_confidence=sum(
                    datum["p_confidence"] for datum in data_for_par
                )
                / len(data_for_par),
            )
            list_for_page_by_par.append(datum)

        return list_for_page_by_par

    def __worker_get_image_block_info_list_for_page__(self, x):
        return self.__get_image_block_info_list_for_page__(x[0], x[1])

    def get_image_block_info_list(self):
        im_list = convert_from_path(self.path, dpi=PDFCompress.DPI_TARGET)
        n_pages = len(im_list)
        log.debug(f"{n_pages=}")
        n_cpus = cpu_count()
        log.debug(f"{n_cpus=}")

        image_block_info_list_list = Pool(processes=n_cpus).map(
            self.__worker_get_image_block_info_list_for_page__,
            enumerate(im_list, start=1),
        )

        image_block_info_list = []
        for image_block_info_list_for_page in image_block_info_list_list:
            if image_block_info_list_for_page:
                image_block_info_list.extend(image_block_info_list_for_page)

        return image_block_info_list

    @staticmethod
    def __get_image_text_from_im__(i_page, im):
        temp_img_path = NamedTemporaryFile(suffix=".png", delete=False).name
        im.save(temp_img_path, format="PNG")

        try:
            image_text = pytesseract.image_to_string(
                temp_img_path, lang="eng", config=TESSERACT_FAST_CONFIG
            )
            return image_text
        except Exception as e:
            log.error(f"[Page {i_page}] Error extracting text from page: {e}")
            return None

    def __worker_get_image_text_from_im__(self, x):
        return self.__get_image_text_from_im__(x[0], x[1])

    @cache
    def get_image_text(self):
        im_list = convert_from_path(self.path, dpi=PDFCompress.DPI_TARGET)
        n_pages = len(im_list)
        log.debug(f"{n_pages=}")
        n_cpus = cpu_count()
        log.debug(f"{n_cpus=}")

        page_text_list = Pool(processes=n_cpus).map(
            self.__worker_get_image_text_from_im__,
            enumerate(im_list, start=1),
        )

        page_text_list = [
            page_text for page_text in page_text_list if page_text is not None
        ]

        text = "\n\n".join(page_text_list)
        return self.__log_text_info_and_return__(text, "Image text")

    @cache
    def get_image_text_from_ocr_block_info_list(self):
        ocr_block_info_list = self.get_image_block_info_list()
        text = "".join(datum["text"] for datum in ocr_block_info_list)
        return self.__log_text_info_and_return__(text, "OCR block text")
