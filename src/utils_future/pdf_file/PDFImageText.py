import time
from functools import cache
from multiprocessing import Pool, cpu_count
from tempfile import NamedTemporaryFile

import pytesseract
from pdf2image import convert_from_path
from utils import Log

from utils_future.pdf_file.PDFCompress import PDFCompress

TESSERACT_FAST_CONFIG = r"""
--oem 1   # LSTM engine (current default; fastest supported in v5)
--psm 6   # assume a uniform block of text; try 7/8/13 if single line/word
-c preserve_interword_spaces=1
-c load_system_dawg=0
-c load_freq_dawg=0
"""

log = Log("PDFImageText")


class PDFImageText:

    @staticmethod
    def __get_image_text_from_image_path__(i_page, image_path):
        t_start = time.time()
        try:
            image_text = pytesseract.image_to_string(
                image_path, lang="eng", config=TESSERACT_FAST_CONFIG
            )
            dt_ms = 1_000 * (time.time() - t_start)
            log.debug(
                f"[Page {i_page}] Extracted {
                    len(image_text):,} B in {
                    dt_ms:,.0f} ms"
            )

            return image_text
        except Exception as e:
            log.error(f"[Page {i_page}] Error extracting text from page: {e}")
            return None

    def __worker__(self, x):
        return self.__get_image_text_from_image_path__(x[0], x[1])

    @cache
    def get_image_text(self):
        im_list = convert_from_path(self.path, dpi=PDFCompress.DPI_TARGET)
        n_pages = len(im_list)
        log.debug(f"{n_pages=}")
        n_cpus = cpu_count()
        log.debug(f"{n_cpus=}")

        temp_image_path_list = []
        for im in im_list:
            temp_img_path = NamedTemporaryFile(
                suffix=".png", delete=False
            ).name
            im.save(temp_img_path, format="PNG")
            temp_image_path_list.append(temp_img_path)

        page_text_list = Pool(processes=n_cpus).map(
            self.__worker__,
            enumerate(temp_image_path_list, start=1),
        )

        page_text_list = [
            page_text for page_text in page_text_list if page_text is not None
        ]

        text = "\n\n".join(page_text_list)
        return self.__log_text_info_and_return__(text, "Image text")
