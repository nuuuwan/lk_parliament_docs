import os
import time
from tempfile import NamedTemporaryFile

import pytesseract
from pdf2image import convert_from_path
from PIL import ImageOps
from pytesseract import Output
from utils import Log

from utils_future.pdf_file.PDFCompressMixin import PDFCompressMixin
from utils_future.pdf_file.PDFTextMixin import PDFTextMixin

TESSERACT_FAST_CONFIG = r"""
--oem 1
--psm 6
"""

log = Log("PDFOCRTextMixin")
os.environ.setdefault("OMP_THREAD_LIMIT", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")


class PDFOCRTextMixin:

    @staticmethod
    def __proprocess_im__(im):
        im = im.convert("L")
        im = ImageOps.autocontrast(im)
        im = im.point(lambda x: 255 if x > 200 else 0, mode="1")
        im.info["dpi"] = (
            PDFCompressMixin.DPI_TARGET,
            PDFCompressMixin.DPI_TARGET,
        )
        temp_img_path = NamedTemporaryFile(suffix=".png", delete=False).name
        im.save(temp_img_path, format="PNG")
        return temp_img_path

    @staticmethod
    def __parse_row__(data, i_page, i, text):
        p_confidence = round(data["conf"][i] / 100.0, 2)

        return dict(
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

    @staticmethod
    def __reduce_by_id__(i_page, group_by_par):
        list_for_page_by_par = []
        for data_for_par in group_by_par.values():
            text = " ".join(d["text"] for d in data_for_par)
            text = PDFTextMixin.__clean_text__(text)
            if not text:
                continue
            datum = dict(
                page_number=i_page,
                bbox=data_for_par[0]["bbox"],
                text=text,
                mean_p_confidence=round(
                    sum(d["p_confidence"] for d in data_for_par)
                    / len(data_for_par),
                    2,
                ),
            )
            if datum:
                list_for_page_by_par.append(datum)

        return list_for_page_by_par

    @staticmethod
    def __map_by_id__(list_for_page):
        group_by_par = {}
        for datum in list_for_page:
            datum_id = "-".join(
                [
                    str(datum[k])
                    for k in ["page_num", "par_num", "block_num", "line_num"]
                ]
            )
            if datum_id not in group_by_par:
                group_by_par[datum_id] = []
            group_by_par[datum_id].append(datum)
        return group_by_par

    @staticmethod
    def __get_ocr_block_info_list_for_page__(i_page, im):
        temp_img_path = PDFOCRTextMixin.__proprocess_im__(im)

        data = pytesseract.image_to_data(
            temp_img_path,
            lang="eng",
            config=TESSERACT_FAST_CONFIG,
            output_type=Output.DICT,
        )
        list_for_page = []
        for i, text in enumerate(data["text"]):
            datum = PDFOCRTextMixin.__parse_row__(data, i_page, i, text)
            if datum:
                list_for_page.append(datum)

        return PDFOCRTextMixin.__reduce_by_id__(
            i_page, PDFOCRTextMixin.__map_by_id__(list_for_page)
        )

    def get_ocr_block_info_list(self):
        t_start = time.perf_counter()
        ocr_block_info_list = []
        for i_page, im in enumerate(
            convert_from_path(self.path, dpi=PDFCompressMixin.DPI_TARGET),
            start=1,
        ):
            ocr_block_info_list_for_page = (
                self.__get_ocr_block_info_list_for_page__(i_page, im)
            )
            if ocr_block_info_list_for_page:
                ocr_block_info_list.extend(ocr_block_info_list_for_page)

        dt = (time.perf_counter() - t_start) * 1_000
        log.debug(f"OCR processing time: {dt:,.0f}ms")
        return ocr_block_info_list
